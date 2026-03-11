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

- 🎯 **Intent Gate** - 意图分析，自动识别 8 种意图类型
- 📍 **Task Routing** - 任务路由，自动选择合适的 Agent 和 Category
- ✅ **Todo Enforcer** - 强制完成，确保任务不被遗漏
- 📚 **Wisdom Accumulation** - 经验累积，跨任务学习
- ⚡ **Parallel Execution** - 并行执行，提高效率

## 安装

```bash
# 安装依赖
pip install pyyaml

# 或复制整个 skill 目录到 OpenClaw
cp -r . ~/.openclaw/workspace/skills/omo
```

## 使用方法

### 命令行

```bash
# 路由任务
python3 omo_tools.py route "实现用户登录"

# 意图分析
python3 omo_tools.py intent "修复这个bug"

# 列出所有 agents
python3 omo_tools.py list-agents

# 列出所有 categories
python3 omo_tools.py list-categories
```

### Python API

```python
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

### MCP 协议

```bash
echo '{"method": "route_task", "params": {"prompt": "任务"}}' | python3 omo_mcp.py
echo '{"method": "list_agents", "params": {}}' | python3 omo_mcp.py
```

## Agent 角色

| Agent | 角色 | 职责 |
|-------|------|------|
| sisyphus | 主协调器 | 规划、调度、统筹 |
| prometheus | 战略规划师 | 访谈式规划 |
| atlas | 执行统筹 | 执行计划、分发任务 |
| hephaestus | 深度工程师 | 自主研究+执行 |
| oracle | 架构顾问 | 架构咨询 |
| explore | 代码探索者 | 快速 grep |
| librarian | 文档管理员 | 文档搜索 |

## Category 路由

| Category | 用途 |
|----------|------|
| visual-engineering | 前端/UI |
| ultrabrain | 深度推理 |
| deep | 复杂编码 |
| quick | 简单快速任务 |
| unspecified-high | 通用复杂 |
| unspecified-low | 通用标准 |

## 路由示例

| 用户输入 | 意图 | Agent | Category |
|----------|------|-------|----------|
| 实现用户登录 | implementation | sisyphus | unspecified-high |
| 修复这个bug | fix | explore | quick |
| 设计系统架构 | architecture | hephaestus | ultrabrain |
| 重构代码 | refactoring | hephaestus | deep |
| 研究这个库 | research | librarian | unspecified-low |
| 改个typo | quick | explore | quick |

## 目录结构

```
skill/
├── SKILL.md          # Skill 文档
├── omo_tools.py      # 工具封装
├── omo.py            # 主入口
├── omo_mcp.py        # MCP 服务器
├── omo_cli.py        # CLI 工具
├── intent_gate.py    # 意图分析
├── todo_enforcer.py  # 强制完成
├── wisdom_accumulator.py  # 经验累积
├── parallel_scheduler.py  # 并行调度
├── agents.yaml       # Agent 角色定义
├── categories.yaml   # Category 路由配置
├── requirements.txt  # Python 依赖
└── prompts/          # Agent prompt 模板
```

## 直接运行

```bash
# 安装依赖
pip install pyyaml

# 运行
python3 omo.py route "你的任务"
python3 omo.py list-agents
python3 omo.py intent "任务描述"
```
