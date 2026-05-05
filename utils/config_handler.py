import yaml  # 导入 YAML 解析库

from utils.path_tool import get_abs_path  # 导入路径工具函数


def load_rag_config(config_path: str = get_abs_path("config/rag.yaml"), encoding: str = "utf-8"):
    """加载 RAG 配置文件（rag.yml）"""
    with open(config_path, "r", encoding=encoding) as f:  # 以只读模式打开 YAML 文件
        return yaml.load(f, Loader=yaml.FullLoader)  # 解析 YAML 内容并返回字典


def load_chroma_config(config_path: str = get_abs_path("config/chroma.yaml"), encoding: str = "utf-8"):
    """加载 Chroma 向量数据库配置文件（chroma.yml）"""
    with open(config_path, "r", encoding=encoding) as f:  # 以只读模式打开 YAML 文件
        return yaml.load(f, Loader=yaml.FullLoader)  # 解析 YAML 内容并返回字典


def load_prompts_config(config_path: str = get_abs_path("config/prompts.yaml"), encoding: str = "utf-8"):
    """加载提示词配置文件（prompts.yml）"""
    with open(config_path, "r", encoding=encoding) as f:  # 以只读模式打开 YAML 文件
        return yaml.load(f, Loader=yaml.FullLoader)  # 解析 YAML 内容并返回字典


def load_agent_config(config_path: str = get_abs_path("config/agent.yaml"), encoding: str = "utf-8"):
    """加载 Agent 配置文件（agent.yml）"""
    with open(config_path, "r", encoding=encoding) as f:  # 以只读模式打开 YAML 文件
        return yaml.load(f, Loader=yaml.FullLoader)  # 解析 YAML 内容并返回字典


# 模块加载时自动读取各配置，可通过模块属性直接访问
rag_conf = load_rag_config()  # 加载 RAG 配置
chroma_conf = load_chroma_config()  # 加载 Chroma 配置
prompts_conf = load_prompts_config()  # 加载提示词配置
agent_conf = load_agent_config()  # 加载 Agent 配置
