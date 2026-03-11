---
name: omo
description: OMO (Oh My OpenClaw) - Multi-Agent Orchestration System. Provides intent analysis, task routing, todo enforcement, and parallel execution. Reference: https://github.com/code-yeongyu/oh-my-openagent
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "install": []
    }
  }
---

# OMO - OpenClaw Multi-Agent Orchestration

🦞 OMO 系统为 OpenClaw 提供多 Agent 编排能力。

## 功能

### 1. 意图分析 (Intent Gate)
自动分析用户输入的真实意图，识别 8 种意图类型并路由到合适的 Agent。

### 2. 任务路由 (Task Routing)
根据意图自动选择合适的 Category 和 Agent。

### 3. Todo 强制完成 (Todo Enforcer)
确保所有任务都被完成，Agent 不能摸鱼。

### 4. 经验累积 (Wisdom Accumulation)
跨任务累积学习，传递给下一个任务。

### 5. 并行执行 (Parallel Execution)
同时运行多个任务，提高效率。

## 工具调用

### 1. Python 直接调用

```python
import sys
sys.path.insert(0, '.')
from omo_tools import route_task, analyze_intent, list_agents

# 路由任务
result = route_task("实现用户登录")
# {
#   "intent": "implementation",
#   "category": "unspecified-high", 
#   "agent": "sisyphus",
#   "model": "xiaomi/MiniMax-M2.5"
# }

# 意图分析
intent = analyze_intent("修复这个bug")
# {
#   "intent": "fix",
#   "category": "quick",
#   "complexity": "medium"
# }

# 列出所有 agents
agents = list_agents()
```

### 2. Shell 命令调用

```bash
# 路由任务
python3 ./omo_tools.py route "实现用户登录"

# 意图分析
python3 ./omo_tools.py intent "修复这个bug"

# 列出所有 agents
python3 ./omo_tools.py list-agents

# 列出所有 categories
python3 ./omo_tools.py list-categories

# 获取 agent prompt
python3 ./omo_tools.py prompt sisyphus
```

### 3. MCP 协议调用

```bash
# 路由任务
echo '{"method": "route_task", "params": {"prompt": "任务"}}' | python3 ../omo_mcp.py

# 意图分析
echo '{"method": "analyze_intent", "params": {"prompt": "任务"}}' | python3 ../omo_mcp.py

# 列出 agents
echo '{"method": "list_agents", "params": {}}' | python3 ../omo_mcp.py
```

## Agent 角色 (10个)

| Agent | 角色 | 职责 |
|-------|------|------|
| sisyphus | 主协调器 | 规划、调度、统筹 |
| prometheus | 战略规划师 | 访谈式规划 |
| atlas | 执行统筹 | 执行计划、分发任务 |
| hephaestus | 深度工程师 | 自主研究+执行 |
| oracle | 架构顾问 | 架构咨询 |
| metis | 差距分析器 | 计划审核 |
| momus | 审核员 | 计划审核 |
| explore | 代码探索者 | 快速 grep |
| librarian | 文档管理员 | 文档搜索 |
| multimodal_looker | 视觉分析师 | 截图分析 |

## Category 路由 (8种)

| Category | 用途 |
|----------|------|
| visual-engineering | 前端/UI |
| ultrabrain | 深度推理 |
| deep | 复杂编码 |
| artistry | 创意任务 |
| quick | 简单快速任务 |
| unspecified-high | 通用复杂 |
| unspecified-low | 通用标准 |
| writing | 写作文档 |

## 路由示例

| 用户输入 | 意图 | Agent | Category |
|----------|------|-------|----------|
| 实现用户登录 | implementation | sisyphus | unspecified-high |
| 修复这个bug | fix | explore | quick |
| 设计系统架构 | architecture | hephaestus | ultrabrain |
| 重构代码 | refactoring | hephaestus | deep |
| 研究这个库 | research | librarian | unspecified-low |
| 改个typo | quick | explore | quick |

## 文件位置

- Skill: `./`
- OMO 核心: `../`
- 工具封装: `./omo_tools.py`
- MCP 服务: `../omo_mcp.py`
