# 导入 Callable 类型注解，用于声明可调用对象的类型
from typing import Callable
# 导入系统提示词和报告提示词的加载函数
from utils.prompt_loader import load_system_prompts, load_report_prompts
# 导入 Agent 状态类型，包含消息列表和运行时状态
from langchain.agents import AgentState
# 导入中间件装饰器和模型请求类型（wrap_tool_call、before_model、dynamic_prompt）
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
# 导入工具调用请求类型，封装了当前执行的工具名称和参数
from langchain.tools.tool_node import ToolCallRequest
# 导入工具消息类型，表示工具执行后返回的消息
from langchain_core.messages import ToolMessage
# 导入运行时类型，用于在工具和中间件之间传递上下文
from langgraph.runtime import Runtime
# 导入 Command 类型，用于在 LangGraph 图中执行跳转或状态更新
from langgraph.types import Command
# 导入自定义日志器，用于记录工具调用和模型执行信息
from utils.logger_handler import logger


# 使用 wrap_tool_call 装饰器声明此函数为工具调用中间件
@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,                                            # 请求的数据封装
        handler: Callable[[ToolCallRequest], ToolMessage | Command],         # 执行的函数本身
) -> ToolMessage | Command:                                                  # 工具执行的监控
    # 记录当前正在执行哪个工具
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    # 记录工具的传入参数
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        # 执行工具本身，获取返回结果
        result = handler(request)
        # 记录工具调用成功
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        # 如果当前执行的是 fill_context_for_report 工具
        if request.tool_call['name'] == "fill_context_for_report":
            # 将运行时上下文的 report 标记设为 True，触发提示词切换到报告模式
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        # 工具调用失败时记录错误日志
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        # 重新抛出异常，由上层处理
        raise e


# 使用 before_model 装饰器声明此函数为模型调用前执行的钩子
@before_model
def log_before_model(
        state: AgentState,       # 整个 Agent 智能体中的状态记录
        runtime: Runtime,        # 记录了整个执行过程中的上下文信息
):         # 在模型执行前输出日志
    # 记录当前消息数量，便于调试 Agent 的思考轮次
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    # 记录最后一条消息的类型和内容（debug 级别），用于排查输入是否正确
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    # before_model 钩子不需要返回值
    return None


# 使用 dynamic_prompt 装饰器声明此函数为动态提示词生成器
@dynamic_prompt                 # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):     # 动态切换提示词
    # 从运行时上下文中获取 report 标记，默认 False
    is_report = request.runtime.context.get("report", False)
    # 如果是报告生成场景
    if is_report:
        # 返回报告生成提示词内容，让 Agent 以报告模式运行
        return load_report_prompts()

    # 否则返回普通对话的系统提示词
    return load_system_prompts()
