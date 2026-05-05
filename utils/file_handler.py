# 导入 hashlib 模块，用于计算文件哈希值
import hashlib
# 从 xml.dom.minidom 导入 Document 类，用于文档类型标注
from xml.dom.minidom import Document
# 从 langchain 社区版导入 PDF 文档加载器和文本文件加载器
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 导入项目自定义的日志器
from utils.logger_handler import logger
# 导入操作系统接口模块，用于文件和路径操作
import os


def get_file_md5_hex(filepath: str):
    """计算文件的 MD5 哈希值（十六进制）"""
    logger.info(f"开始计算文件 MD5: {filepath}")

    # 检查文件路径是否存在
    if not os.path.exists(filepath):
        # 文件不存在，记录错误日志并返回
        logger.error(f"文件不存在: {filepath}")
        return None

    # 检查路径是否指向一个文件（而不是目录）
    if not os.path.isfile(filepath):
        # 路径不是文件，记录错误日志并返回
        logger.error(f"路径不是文件: {filepath}")
        return None

    # 创建一个 MD5 哈希对象
    md5_obj = hashlib.md5()

    # 设置每次读取的块大小为 4KB
    chunk_size = 4096
    try:
        # 以二进制只读模式打开文件
        with open(filepath, "rb") as f:
            # 循环读取文件内容，每次读取一个块
            while chunk := f.read(chunk_size):
                # 将读取到的块数据更新到 MD5 对象中
                md5_obj.update(chunk)

            # 计算最终的 MD5 十六进制摘要
            md5_hex = md5_obj.hexdigest()
            # 返回 MD5 值
            logger.info(f"文件 MD5 计算完成: {filepath}")
            return md5_hex

    except Exception:
        # 读取过程中发生异常，记录异常日志（自动包含堆栈追踪）
        logger.exception(f"读取文件失败: {filepath}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """列出指定目录下所有符合类型要求的文件"""
    # 初始化空列表，用于存放符合条件的文件路径
    files = []
    # 检查路径是否是一个目录
    if not os.path.isdir(path):
        # 不是目录，记录错误日志并返回
        logger.error(f"路径不是目录: {path}")
        return []
    # 遍历目录中的所有条目
    for f in os.listdir(path):
        # 检查文件是否以允许的类型结尾
        if f.endswith(allowed_types):
            # 符合条件，将完整路径添加到列表中
            files.append(os.path.join(path, f))

    # 返回符合条件的文件路径元组
    return tuple(files)


def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    """加载 PDF 文件并返回 Document 列表"""
    # 使用 PyPDFLoader 加载 PDF，支持密码保护文件
    return PyPDFLoader(filepath, password=passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    """加载文本文件并返回 Document 列表"""
    # 使用 TextLoader 以 UTF-8 编码加载文本文件
    return TextLoader(filepath, encoding="utf-8").load()
