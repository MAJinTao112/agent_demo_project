# RAG + Agent Demo Project

基于 LangChain + 阿里云 DashScope（通义千问）的 RAG 问答与 Agent 报告生成系统。

作者：[haitao223](https://github.com/haitao223)

> 一个很简陋的 Demo，代码粗糙、逻辑简单，仅供学习参考。

## 目录结构

```
├── app.py                         # Streamlit 前端
├── agent/
│   ├── react_agent.py             # Agent 执行器（create_agent + 中间件）
│   └── tools/
│       ├── agent_tools.py         # 7 个工具定义
│       └── middleware.py          # 中间件（日志、提示词切换）
├── config/                        # YAML 配置
├── data/                          # 知识库文档 + 使用记录 CSV
├── model/factory.py               # 模型工厂
├── prompts/                       # 提示词模板
├── rag/
│   ├── rag_service.py             # RAG 服务编排
│   └── vector_store.py            # 向量数据库服务
└── utils/                         # 工具模块
```

## 快速开始

```bash
pip install langchain-chroma langchain-community langchain-core langchain-text-splitters dashscope pypdf streamlit
```

编辑 `config/rag.yaml` 填入 API Key，然后：

```bash
# 加载知识库文档到向量库
python rag/vector_store.py

# RAG 问答测试
python rag/rag_service.py

# Agent 工具测试
python agent/tools/agent_tools.py

# 启动 Web 界面
streamlit run app.py
```

## 架构

```
用户输入
  ↓
app.py (Streamlit)
  ↓
ReactAgent (create_agent + LangGraph)
  ├── 中间件: 工具监控 → 模型调用前日志 → 动态提示词切换
  ├── 工具: rag_summarize, get_weather, get_user_location, get_user_id,
  │         get_current_month, fetch_external_data, fill_context_for_report
  └── ReAct 循环: 思考 → 行动 → 观察 → 再思考（最多 5 轮）
       ↓
RagSummarizeService
  ├── Chroma 向量检索（top-3）
  ├── 上下文组装
  └── ChatTongyi（通义千问）生成回答
```

## 工具列表

| 工具 | 参数 | 说明 |
|------|------|------|
| `rag_summarize` | query | 检索知识库并生成回答 |
| `get_weather` | city | 查询天气（模拟） |
| `get_user_location` | 无 | 随机返回城市 |
| `get_user_id` | 无 | 随机返回用户 ID |
| `get_current_month` | 无 | 随机返回月份 |
| `fetch_external_data` | user_id, month | 查询使用记录（CSV） |
| `fill_context_for_report` | 无 | 触发报告上下文注入 |

## 配置

| 文件 | 主要配置项 |
|------|-----------|
| `config/rag.yaml` | 模型名、API Key |
| `config/chroma.yaml` | 向量库参数、文本分块 |
| `config/agent.yaml` | 外部数据路径 |
| `config/prompts.yaml` | 提示词文件路径 |

## 数据

- `data/` — 6 份扫地机器人知识库文档（选购、使用、故障、维护等）
- `data/external/records.csv` — 10 用户 × 12 月的模拟使用记录

## 提示词模板

- `prompts/main_prompt.txt` — Agent 系统提示词（ReAct 框架 + 工具定义）
- `prompts/rag_summarize.txt` — RAG 摘要提示词（注入 {{input}} 和 {{context}}）
- `prompts/report_prompt.txt` — 报告生成提示词（Markdown 输出）

---

*欲买桂花同载酒，终不似，少年游。*
