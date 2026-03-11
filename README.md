# oh-my-opencode-openclaw

🦞 **Oh My OpenCode for OpenClaw** - Multi-Agent Orchestration System for OpenClaw

参考 [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) 实现的 Agent 编排系统，为 OpenClaw 提供多 Agent 协作能力。

[![GitHub stars](https://img.shields.io/github/stars/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw/network)
[![License](https://img.shields.io/github/license/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)

## 功能

- 🎯 **Intent Gate** - 意图分析，自动识别 8 种意图类型
- 📍 **Task Routing** - 任务路由，自动选择合适的 Agent 和 Category
- ✅ **Todo Enforcer** - 强制完成，确保任务不被遗漏
- 📚 **Wisdom Accumulation** - 经验累积，跨任务学习
- ⚡ **Parallel Execution** - 并行执行，提高效率

## 🚀 快速开始

### 方式一：克隆使用

```bash
# 克隆仓库
git clone https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw.git
cd oh-my-opencode-openclaw

# 安装依赖
pip install -r requirements.txt

# 直接运行
python3 omo.py route "实现用户登录"
python3 omo.py list-agents
```

### 方式二：作为 OpenClaw Skill 使用

```bash
# 复制 skill 目录到 OpenClaw
cp -r skill/ ~/.openclaw/workspace/skills/omo
```

然后在 OpenClaw 中就可以直接使用 OMO 功能了！

### 方式三：作为 MCP 使用

在 OpenClaw 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "omo": {
      "command": "python3",
      "args": ["path/to/oh-my-opencode-openclaw/omo_mcp.py"]
    }
  }
}
```

## 📖 使用方法

### 命令行

```bash
# 路由任务（自动意图分析）
python3 omo.py route "实现用户登录"

# 意图分析
python3 omo.py intent "修复这个bug"

# 列出所有 agents
python3 omo.py list-agents

# 列出所有 categories
python3 omo.py list-categories

# 获取 agent prompt
python3 omo.py prompt sisyphus
```

### Python API

```python
from omo import OMOSystem

omo = OMOSystem()
result = omo.route_task("实现用户登录")
print(result)
# {
#   "intent": "implementation",
#   "category": "unspecified-high",
#   "agent": "sisyphus",
#   "model": "xiaomi/MiniMax-M2.5"
# }
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

## 目录结构

```
oh-my-opencode-openclaw/
├── omo.py                 # 统一入口
├── omo_mcp.py             # MCP 服务器
├── omo_cli.py             # CLI 工具
├── tools.sh               # Shell 工具封装
├── agents.yaml            # Agent 角色定义
├── categories.yaml        # Category 路由配置
├── intent_gate.py         # 意图分析
├── todo_enforcer.py       # 强制完成
├── wisdom_accumulator.py  # 经验累积
├── parallel_scheduler.py  # 并行调度
├── requirements.txt       # Python 依赖
├── prompts/               # Agent prompt 模板
├── skill/                 # OpenClaw Skill
│   ├── SKILL.md
│   ├── omo_tools.py
│   └── mcp.json
└── README.md
```

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=Xingyu-Romantic/oh-my-opencode-openclaw&type=Date)](https://star-history.com/#Xingyu-Romantic/oh-my-opencode-openclaw)

---

🦞 Built with ❤️ for OpenClaw
