# oh-my-opencode-openclaw

🦞 **Oh My OpenCode for OpenClaw** - Multi-Agent Orchestration System for OpenClaw

参考 [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) 实现的 Agent 编排系统，为 OpenClaw 提供多 Agent 协作能力。

[![GitHub stars](https://img.shields.io/github/stars/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw/network)
[![GitHub issues](https://img.shields.io/github/issues/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw/issues)
[![License](https://img.shields.io/github/license/Xingyu-Romantic/oh-my-opencode-openclaw?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)

## ⭐ Stars 增长趋势

```
stars
   ^
 10 |                    ╭──╮
  9 |               ╭───╯  ╰───╮
  8 |          ╭───╯              ╰───╮
  7 |     ╭───╯                      ╰───
  6 |  ╭─╯
  5 |─╯
   +--------------------------------→ time
     Jan  Feb  Mar  Apr  May  Jun
```

> 📊 目标：让 OMO 成为 OpenClaw 生态的核心编排系统！

## 功能

- 🎯 **Intent Gate** - 意图分析，自动识别 8 种意图类型
- 📍 **Task Routing** - 任务路由，自动选择合适的 Agent 和 Category
- ✅ **Todo Enforcer** - 强制完成，确保任务不被遗漏
- 📚 **Wisdom Accumulation** - 经验累积，跨任务学习
- ⚡ **Parallel Execution** - 并行执行，提高效率

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Xingyu-Romantic/oh-my-opencode-openclaw.git
cd oh-my-opencode-openclaw

# 安装依赖 (可选)
pip install pyyaml
```

### 使用方法

```bash
# 路由任务
python3 omo.py route "实现用户登录"

# 意图分析
python3 omo.py intent "修复这个bug"

# 列出所有 agents
python3 omo.py list-agents

# 列出所有 categories
python3 omo.py list-categories
```

### Python API

```python
import sys
sys.path.insert(0, '/path/to/oh-my-opencode-openclaw')
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
| metis | 差距分析器 | 计划审核 |
| momus | 审核员 | 计划审核 |
| explore | 代码探索者 | 快速 grep |
| librarian | 文档管理员 | 文档搜索 |
| multimodal_looker | 视觉分析师 | 截图分析 |

## Category 路由

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

## 工作流

### Ultrawork 模式
```
ultrawork 或 ulw
```
自动分析、执行、验证，直到完成。

### Prometheus 模式
```
@plan "任务描述"
```
访谈式规划，然后执行。

## 目录结构

```
oh-my-opencode-openclaw/
├── omo.py                 # 统一入口
├── omo_mcp.py             # MCP 服务器
├── tools.sh               # Shell 工具封装
├── agents.yaml            # Agent 角色定义
├── categories.yaml        # Category 路由配置
├── intent_gate.py         # 意图分析
├── todo_enforcer.py       # 强制完成
├── wisdom_accumulator.py  # 经验累积
├── parallel_scheduler.py  # 并行调度
├── prompts/               # Agent prompt 模板
├── skill/                 # OpenClaw Skill
│   ├── SKILL.md
│   ├── omo_tools.py
│   └── mcp.json
└── README.md
```

## 集成到 OpenClaw

### 作为 Skill 使用

将 `skill/` 目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r skill/ ~/.openclaw/workspace/skills/omo
```

### 作为 MCP 使用

配置 `mcp.json` 到 OpenClaw 的 MCP 配置中。

## 贡献

欢迎提交 Issue 和 Pull Request！

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=Xingyu-Romantic/oh-my-opencode-openclaw&type=Date)](https://star-history.com/#Xingyu-Romantic/oh-my-opencode-openclaw)

---

🦞 Built with ❤️ for OpenClaw
