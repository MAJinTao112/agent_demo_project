# 导入 os.path 模块，用于检查文件或目录是否存在
import os.path

# 导入 Chroma 向量数据库，用于存储和检索向量化的文档
from langchain_chroma import Chroma
# 导入 Document 类，LangChain 统一的数据结构，包含 page_content 和 metadata
from langchain_core.documents import Document
# 导入递归字符文本分割器，用于将长文本按指定分隔符切分成块
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 导入自定义的日志器，用于记录程序运行信息
from utils.logger_handler import logger
# 导入 Chroma 数据库的配置项，如集合名称、持久化目录等
from utils.config_handler import chroma_conf
# 导入嵌入模型实例，用于将文本转换为向量
from model.factory import embed_model
# 导入文件工具函数：TXT加载器、PDF加载器、列出指定类型文件、计算文件 MD5
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
# 导入路径工具函数，用于获取项目根目录下的绝对路径
from utils.path_tool import get_abs_path


# 定义向量数据库服务类，封装文档加载、分割、存储和检索功能
class VectorStoreService:
    # 初始化方法，创建 Chroma 数据库实例和文本分割器
    def __init__(self):
        # 创建 Chroma 向量数据库实例，指定集合名称、嵌入函数和持久化目录
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],       # 集合名称，用于区分不同数据集
            embedding_function=embed_model,                      # 嵌入函数，将文本转为向量
            persist_directory=chroma_conf["persist_directory"],  # 数据持久化目录

        )
        # 创建递归字符文本分割器，用于将文档拆分成小块
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],       # 每个文本块的最大字符数
            chunk_overlap=chroma_conf["chunk_overlap"], # 相邻块之间的重叠字符数
            separators=chroma_conf["separator"],        # 分割符优先级列表，按顺序尝试切割
            length_function=len                         # 计算文本长度的函数，默认 len
        )

    # 获取向量检索器，用于根据查询检索最相似的文档
    def get_retriever(self):
        # 调用 Chroma 的 as_retriever 方法，设置返回前 k 个最相似文档
        return self.vector_store.as_retriever(search_kwargs={"k":chroma_conf["k"]})


    # 加载文档的主方法：遍历目录中的文件，检查变更，分割后存入向量数据库
    def load_document(self):
        # 内部函数：检查指定 MD5 值是否已记录（即文件是否已经加载过）
        def check_md5_hex(md5_for_check: str):
            # 如果 MD5 记录文件不存在，则创建空文件并返回 False（表示需加载）
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 以写入模式创建空文件，然后关闭
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w",encoding="utf-8").close()
                return False

            # 以只读模式打开 MD5 记录文件
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                # 逐行读取文件内容
                for line in f.readlines():
                    line = line.strip()  # 去除行首尾空白字符
                    if line == md5_for_check:  # 如果找到匹配的 MD5 值
                        return True  # 文件已存在，无需重新加载

                return False  # 未找到匹配，文件需要加载

        # 内部函数：将文件 MD5 值追加写入记录文件
        def save_md5_hex(md5_for_check: str):
            # 以追加模式打开 MD5 记录文件
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_check + "\n")  # 写入 MD5 值并换行

        # 内部函数：根据文件扩展名选择合适的加载器，返回 Document 列表
        def get_file_documents(read_path:str):
            # 如果是 .txt 文件，使用 TXT 加载器
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            # 如果是 .pdf 文件，使用 PDF 加载器
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)

            # 不支持的文件类型返回空列表
            return []

        # 获取允许加载的文件路径列表，按配置中的文件类型过滤
        allowed_files_path:list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),              # 数据源目录
            tuple(chroma_conf["allow_knowledge_file_type"])      # 允许的文件类型
        )

        # 遍历所有允许的文件
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)  # 计算当前文件的 MD5 值

            # 如果 MD5 已存在，说明文件已加载过，跳过该文件
            if check_md5_hex(md5_hex):
                logger.info(f"文档已存在，跳过: {path}")
                continue
            try:
                # 读取文件内容，返回 Document 列表
                documents: list[Document] = get_file_documents(path)

                # 如果未读取到任何文档，记录警告并跳过
                if not documents:
                    logger.warning(f"未从文件中读取到任何文档: {path}")
                    continue
                # 将文档分割成更小的块，便于向量检索
                split_document: list[Document] = self.splitter.split_documents(documents)

                # 如果分割后为空，记录警告并跳过
                if not split_document:
                    logger.warning(f"文档切分后为空: {path}")
                    continue

                # 将分割后的文档块添加到向量数据库
                self.vector_store.add_documents(split_document)
                # 记录该文件的 MD5，下次运行时跳过
                save_md5_hex(md5_hex)
                logger.info(f"成功加载文档: {path}")
            except Exception as e:
                logger.error(f"加载文档失败 {path}: {e}", exc_info=True)


# 当直接运行此脚本时执行以下代码
if __name__ == "__main__":
    # 创建向量数据库服务实例
    vs = VectorStoreService()

    # 加载所有文档到向量数据库
    vs.load_document()

    # 获取向量检索器
    retriever = vs.get_retriever()

    # 使用检索器查询与"你是什么模型"相关的文档
    res = retriever.invoke("你是什么模型"
                           )

    # 遍历检索结果，打印每个文档的文本内容
    for doc in res:
        print(doc.page_content)
        print("=" * 50)
