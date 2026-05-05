# RAG + Agent Demo Project

基于 LangChain + 阿里云 DashScope（通义千问）的 RAG 问答与 Agent 报告生成系统。

作者：[haitao223](https://github.com/haitao223)

> 一个很简陋的 Demo，代码粗糙、逻辑简单，仅供学习参考。

## 目录结构

```
├── agent/tools/agent_tools.py    # Agent 工具集
├── config/                       # YAML 配置（模型、向量库、提示词、Agent）
├── data/                         # 知识库文档 + 外部使用记录 CSV
├── model/factory.py              # 模型工厂（抽象工厂模式）
├── prompts/                      # 提示词模板
├── rag/
│   ├── rag_service.py            # RAG 服务编排
│   └── vector_store.py           # 向量数据库服务
└── utils/                        # 工具（配置、文件、日志、路径、提示词加载）
```

## 快速开始

```bash
pip install langchain-chroma langchain-community langchain-core langchain-text-splitters dashscope pypdf
```

编辑 `config/rag.yaml`，填入 API Key，然后：

```bash
# 加载知识库文档到 Chroma
python rag/vector_store.py

# RAG 问答
python rag/rag_service.py

# 测试 Agent 工具
python agent/tools/agent_tools.py
```

## 两种工作模式

### RAG 问答

用户提问 → 从 Chroma 检索 top-3 相关文档 → 组装上下文 → 调大模型生成回答。

### Agent 报告生成

通过 ReAct 框架按顺序调用工具：获取用户 ID → 获取月份 → 注入上下文 → 查询使用记录 → 检索知识库 → 生成 Markdown 报告。

## 工具列表

| 工具 | 说明 |
|------|------|
| `rag_summarize` | 检索知识库并生成回答 |
| `get_weather` | 查询天气（模拟） |
| `get_user_location` | 用户所在城市 |
| `get_user_id` | 用户 ID |
| `get_current_month` | 当前月份 |
| `fetch_external_data` | 查询用户使用记录 |
| `fill_context_for_report` | 触发报告上下文注入 |

## 配置

- 模型配置：`config/rag.yaml`
- 向量库配置：`config/chroma.yaml`
- Agent 配置：`config/agent.yaml`
- 提示词路径：`config/prompts.yaml`
- 提示词模板：`prompts/` 目录

---

*欲买桂花同载酒，终不似，少年游。*
