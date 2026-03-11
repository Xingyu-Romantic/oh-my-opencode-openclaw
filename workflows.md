# OMO 工作流系统

## 使用模式

### 1. Ultrawork 模式 (懒人模式)
```
ultrawork 或 ulw
```
Agent 自动分析任务、探索代码库、研究模式、实现功能、用诊断验证。不停直到完成。

### 2. Prometheus 模式 (精确模式)
```
@plan "你的任务"
```
Prometheus 访谈你，问澄清问题，识别范围歧义，在写代码前构建详细计划。

然后运行：
```
/start-work
```
Atlas 接管，执行计划，分发任务给 subagents，验证完成度。

### 3. 直接委托模式
```
task(category: "visual-engineering", prompt: "...")
```
直接指定 category，让系统自动选择合适的 agent 和模型。

---

## 工作流状态机

```
用户请求
    ↓
[Intent Gate] - 分析真实意图
    ↓
    ├─→ 简单任务 → 直接执行
    │
    ├─→ ultrawork → Sisyphus 自动执行
    │
    └─→ 复杂任务
            ↓
        [Prometheus 访谈]
            ↓
        [Metis 差距分析]
            ↓
        [Momus 审核] (可选)
            ↓
        [生成计划]
            ↓
        /start-work
            ↓
        [Atlas 执行]
            ↓
        [并行分发任务]
            ↓
        [验证结果]
            ↓
        [累积学习]
            ↓
        [报告完成]
```

---

## Todo Enforcer 机制

当 Agent 有未完成的 todos 时，系统强制提醒：

```
[系统提醒 - TODO 继续]

你有未完成的 todos！完成所有后再回复：
- [ ] 实现用户服务 ← 进行中
- [ ] 添加验证
- [ ] 编写测试

未完成所有 todos 前不要回复。
```

---

## Wisdom Accumulation (经验累积)

每个任务完成后，Atlas 提取学习内容传递给后续 agents：

```
.sisyphus/notepads/{plan-name}/
├── learnings.md      # 模式、约定、成功方法
├── decisions.md      # 架构选择和理由
├── issues.md         # 遇到的问题、阻塞、坑
├── verification.md   # 测试结果、验证结果
└── problems.md       # 未解决的问题、技术债务
```
