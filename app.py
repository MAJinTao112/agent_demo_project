# 导入 time 模块，用于在流式输出时添加逐字打印的延迟
import time

# 导入 Streamlit，用于构建 Web 聊天界面
import streamlit as st
# 导入 ReactAgent，封装了 LangChain Agent 的执行逻辑
from agent.react_agent import ReactAgent


# 设置页面标题
st.title("智扫通机器人智能客服")
# 添加分割线，区分标题和聊天区域
st.divider()

# 检查会话状态中是否已有 Agent 实例，没有则创建（Streamlit 每次交互会重新运行脚本）
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 检查会话状态中是否已有消息列表，没有则初始化为空列表
if "message" not in st.session_state:
    st.session_state["message"] = []

# 遍历历史消息，逐条显示在聊天界面上
for message in st.session_state["message"]:
    # 根据角色（user/assistant）显示对应样式的消息气泡
    st.chat_message(message["role"]).write(message["content"])

# 创建聊天输入框，等待用户输入
prompt = st.chat_input()

# 如果用户输入了内容，处理该条消息
if prompt:
    # 在界面上显示用户的消息
    st.chat_message("user").write(prompt)
    # 将用户消息存入会话历史
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 用于缓存流式输出的每个块
    response_messages = []
    # 显示加载动画，表示模型正在处理
    with st.spinner("智能客服思考中..."):
        # 调用 Agent 的流式执行方法，返回一个生成器
        res_stream = st.session_state["agent"].execute_stream(prompt)

        # 定义捕获函数：遍历生成器，缓存每个块，并以逐字方式输出
        def capture(generator, cache_list):
            # 遍历流式生成的每个块
            for chunk in generator:
                # 将块内容追加到缓存列表，用于后续保存到会话历史
                cache_list.append(chunk)
                # 逐字输出，模拟打字效果
                for char in chunk:
                    # 每字间隔 10 毫秒
                    time.sleep(0.01)
                    yield char

        # 以流式方式在界面上显示助手回复
        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        # 将完整的回复内容存入会话历史（取最后一个缓存块）
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        # 重新运行脚本，刷新界面显示最新消息
        st.rerun()
