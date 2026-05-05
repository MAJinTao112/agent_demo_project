# 导入 LangChain 的 Agent 工厂函数，基于 LangGraph StateGraph 构建 Agent 执行图
from langchain.agents import create_agent
# 导入聊天模型实例（通义千问），用于 Agent 的推理和工具调用
from model.factory import chat_model
# 导入系统提示词加载函数，从 prompts/main_prompt.txt 读取
from utils.prompt_loader import load_system_prompts
# 导入所有 Agent 工具
from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
# 导入中间件：工具监控、模型调用日志、动态提示词切换
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


# 定义 Agent 执行器类，封装 LangChain Agent 的创建和流式执行
class ReactAgent:
    # 初始化方法：创建 Agent 实例
    def __init__(self):
        # 使用 create_agent 构建 Agent 图
        self.agent = create_agent(
            model=chat_model,                                              # 底层推理模型
            system_prompt=load_system_prompts(),                           # Agent 系统提示词
            tools=[rag_summarize, get_weather, get_user_location, get_user_id,            # 可用工具列表
                   get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],              # 中间件链
        )

    # 流式执行方法：接收用户查询，以生成器方式逐块返回 Agent 回复
    def execute_stream(self, query: str):
        # 构造 LangGraph 标准输入格式，包含消息列表
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        # 调用 Agent 图的 stream 方法，流式获取执行结果
        # context 参数携带运行时上下文，用于中间件做提示词切换（report=False 表示非报告模式）
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            # 从当前 chunk 中取出最新的消息
            latest_message = chunk["messages"][-1]
            # 如果消息有内容，逐块产出
            if latest_message.content:
                yield latest_message.content.strip() + "\n"


# 直接运行此脚本时的测试入口
if __name__ == '__main__':
    # 创建 Agent 实例
    agent = ReactAgent()

    # 流式执行报告生成查询，逐块打印输出
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
