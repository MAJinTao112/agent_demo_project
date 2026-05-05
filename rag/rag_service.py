# 导入 List 类型注解，用于声明方法返回列表类型
from typing import List

# 导入字符串输出解析器，将模型返回内容解析为纯文本字符串
from langchain_core.output_parsers import StrOutputParser
# 导入 PromptTemplate 类，用于从模板字符串创建提示词模板
from langchain_core.prompts import PromptTemplate
# 导入 RunnableLambda，将普通函数包装为 LangChain 链中可运行的节点
from langchain_core.runnables import RunnableLambda
# 导入 Document 类，LangChain 统一的数据结构，包含 page_content 和 metadata
from langchain_core.documents import Document

# 导入聊天模型实例，用于生成回答
from model.factory import chat_model
# 导入向量数据库服务类，用于检索相关文档
from rag.vector_store import VectorStoreService
# 导入 RAG 提示词加载函数，从配置中读取提示词模板
from utils.prompt_loader import load_rag_prompts


# 打印 prompt 并原样返回，用于调试链中的 prompt 内容
def print_prompt(prompt_text: str) -> str:
    # 打印 prompt 开始标记
    print(f"\n===== Prompt =====")
    # 打印 prompt 具体内容
    print(prompt_text)
    # 打印 prompt 结束标记
    print("==================\n")
    # 将 prompt 原样返回，不影响链中后续节点
    return prompt_text


# 定义 RAG 总结服务类，整合检索、组装提示词和模型生成
class RagSummarizeService(object):
    # 初始化方法：创建向量库实例、检索器、提示词模板和链
    def __init__(self):
        # 创建向量数据库服务实例
        self.vector_store = VectorStoreService()
        # 获取向量检索器，用于根据查询检索相关文档
        self.retriver = self.vector_store.get_retriever()
        # 从配置中加载 RAG 提示词模板文本
        self.prompt_text = load_rag_prompts()
        # 将模板文本转为 PromptTemplate 对象，支持变量替换
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        # 保存聊天模型实例
        self.model = chat_model
        # 初始化处理链：模板 → 打印 → 模型 → 解析
        self.chain = self._init_chain()

    # 初始化 LangChain 处理链
    def _init_chain(self):
        # 构建链：提示词模板 → 打印调试 → 聊天模型 → 字符串解析
        chain = self.prompt_template | RunnableLambda(print_prompt) | self.model | StrOutputParser()
        # 返回构建好的链
        return chain

    # 根据查询检索相关文档，返回 Document 列表
    def retrieve_docs(self, query: str) -> List[Document]:
        # 调用检索器的 invoke 方法执行检索
        return self.retriver.invoke(query)

    # RAG 总结方法：检索文档 → 组装上下文 → 调用链生成回答
    def rag_summarize(self, query: str) -> str:
        # 根据用户查询检索相关文档
        context_docs = self.retrieve_docs(query)

        # 初始化上下文字符串
        context = ""
        # 计数器，用于给每篇参考资料编号
        counter = 0
        # 遍历检索到的文档，拼装成上下文
        for doc in context_docs:
            counter += 1
            # 每篇文档格式：编号 + 内容 + 元数据
            context += f"【参考资料{counter}】：参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        # 调用链，传入用户查询和拼接好的上下文
        return self.chain.invoke(
            {
                "input": query,    # 用户输入的问题
                "context": context, # 检索到的参考上下文
            }
        )

# 当直接运行此脚本时执行以下代码
if __name__ == '__main__':
    # 创建 RAG 总结服务实例
    rag = RagSummarizeService()

    # 调用 rag_summarize 方法并打印结果
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))
