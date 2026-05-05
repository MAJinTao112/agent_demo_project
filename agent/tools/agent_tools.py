# 导入 os 模块，用于检查文件路径是否存在
import os
# 导入自定义日志器，用于记录程序运行信息
from utils.logger_handler import logger
# 导入 LangChain 的 tool 装饰器，用于将函数声明为可被 Agent 调用的工具
from langchain_core.tools import tool
# 导入 RAG 总结服务，用于检索文档并生成回答
from rag.rag_service import RagSummarizeService
# 导入 random 模块，用于模拟随机选择
import random
# 导入 Agent 配置，如外部数据文件路径
from utils.config_handler import agent_conf
# 导入路径工具函数，用于获取项目根目录下的绝对路径
from utils.path_tool import get_abs_path

# 创建 RAG 总结服务全局实例，供工具函数调用
rag = RagSummarizeService()

# 模拟用户 ID 列表，用于测试
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
# 模拟月份列表，用于测试
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

# 用于缓存外部数据的全局字典，读取文件后填充
external_data = {}


# 声明为 Agent 工具：从向量存储中检索参考资料并生成回答
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    # 调用 RAG 服务，传入用户查询，返回基于检索结果的回答
    return rag.rag_summarize(query)


# 声明为 Agent 工具：获取指定城市的天气信息（模拟数据）
@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    # 返回模拟的天气数据字符串
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"


# 声明为 Agent 工具：随机返回一个用户所在城市（模拟）
@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    # 从深圳、合肥、杭州中随机选一个
    return random.choice(["深圳", "合肥", "杭州"])


# 声明为 Agent 工具：随机返回一个用户 ID（模拟）
@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    # 从预定义的用户 ID 列表中随机选一个
    return random.choice(user_ids)


# 声明为 Agent 工具：随机返回一个月份（模拟）
@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    # 从预定义的月份列表中随机选一个
    return random.choice(month_arr)


# 从外部数据文件加载数据，填充到全局 external_data 字典
def generate_external_data():
    """
    外部数据文件格式（CSV）：
    "user_id": {
        "month" : {"特征": xxx, "效率": xxx, ...}
        "month" : {"特征": xxx, "效率": xxx, ...}
        ...
    }
    :return:
    """
    # 只在第一次调用时加载，避免重复读取文件
    if not external_data:
        # 获取外部数据文件的绝对路径
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        # 如果文件不存在，抛出异常
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        # 以只读模式打开 CSV 文件
        with open(external_data_path, "r", encoding="utf-8") as f:
            # 跳过表头行（[1:]），逐行读取数据
            for line in f.readlines()[1:]:
                # 去除首尾空白，按逗号分割
                arr: list[str] = line.strip().split(",")

                # 提取各字段，去除引号
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                # 如果该用户首次出现，初始化空字典
                if user_id not in external_data:
                    external_data[user_id] = {}

                # 按用户 ID → 月份 存储该条记录
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


# 声明为 Agent 工具：从外部系统获取指定用户在指定月份的使用记录
@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    # 确保外部数据已加载
    generate_external_data()

    try:
        # 返回对应用户和月份的数据
        return external_data[user_id][month]
    except KeyError:
        # 未找到数据，记录警告日志并返回空字符串
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""


# 声明为 Agent 工具：触发中间件注入报告生成的上下文信息
@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    # 返回确认字符串，表示上下文注入已触发
    return "fill_context_for_report已调用"


# 测试用例
if __name__ == "__main__":
    print(fetch_external_data.invoke({"user_id": "1005", "month": "2025-06"}))
