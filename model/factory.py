# 导入 ABC 和 abstractmethod，用于定义抽象基类
from abc import ABC, abstractmethod
# 导入 Optional，用于类型注解，表示返回值可能为 None
from typing import Optional

# 嵌入模型的抽象接口，所有嵌入模型必须实现 embed_documents 和 embed_query
from langchain_core.embeddings import Embeddings
# 通义千问聊天模型的基类，所有通义千问聊天模型的抽象接口
from langchain_community.chat_models.tongyi import BaseChatModel
# 导入 RAG 相关的配置项，如模型名称
from utils.config_handler import rag_conf
# 阿里云 DashScope 的嵌入模型具体实现
from langchain_community.embeddings import DashScopeEmbeddings
# 通义千问聊天模型的具体实现
from  langchain_community.chat_models.tongyi import ChatTongyi
# 抽象基类：定义所有模型工厂的统一接口
class BaseModelFactory(ABC):
    # 声明抽象方法，子类必须实现此方法
    @abstractmethod
    # generate 方法返回一个嵌入模型或聊天模型的实例
    def generate(self)-> Optional[Embeddings | BaseChatModel]:
        # 抽象方法没有具体实现，由子类负责
        pass



# 聊天模型工厂：专门创建聊天模型实例
class ChatModelFactory(BaseModelFactory):
    # 实现父类的抽象方法
    def generate(self)-> Optional[Embeddings | BaseChatModel]:
        # 根据配置创建通义千问聊天模型实例，传入 API Key
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=rag_conf["dashscope_api_key"],
        )


# 嵌入模型工厂：专门创建嵌入模型实例
class EmbeddingsFactory(BaseModelFactory):
    # 实现父类的抽象方法
    def generate(self)-> Optional[Embeddings | BaseChatModel]:
        # 根据配置创建 DashScope 嵌入模型实例，传入 API Key
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=rag_conf["dashscope_api_key"],
        )


# 创建全局单例：聊天模型实例
chat_model = ChatModelFactory().generate()
# 创建全局单例：嵌入模型实例
embed_model = EmbeddingsFactory().generate()


