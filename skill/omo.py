#!/usr/bin/env python3
"""
OMO - OpenClaw Multi-Agent Orchestration System
统一入口，整合所有功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from intent_gate import IntentGate, IntentType
from todo_enforcer import TodoEnforcer
from wisdom_accumulator import WisdomAccumulator
from parallel_scheduler import ParallelScheduler
import yaml
import json

class OMOSystem:
    """OMO 系统主类"""
    
    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path("omo-system")
        
        # 加载配置
        self._load_config()
        
        # 初始化组件
        self.intent_gate = IntentGate()
        self.wisdom = WisdomAccumulator(str(self.workspace_dir / "notepads"))
        
        # 当前会话的组件
        self.current_todo: TodoEnforcer = None
        self.current_scheduler: ParallelScheduler = None
    
    def _load_config(self):
        """加载配置"""
        # Agents
        agents_file = self.workspace_dir / "agents.yaml"
        if agents_file.exists():
            with open(agents_file) as f:
                self.agents = yaml.safe_load(f).get("agents", {})
        else:
            self.agents = {}
        
        # Categories
        categories_file = self.workspace_dir / "categories.yaml"
        if categories_file.exists():
            with open(categories_file) as f:
                self.categories = yaml.safe_load(f).get("categories", {})
        else:
            self.categories = {}
    
    # ============ Intent Gate ============
    
    def analyze_intent(self, prompt: str) -> dict:
        """分析用户意图"""
        return self.intent_gate.analyze(prompt)
    
    # ============ Todo Enforcer ============
    
    def create_todo_session(self, session_id: str = "default") -> TodoEnforcer:
        """创建 todo 会话"""
        self.current_todo = TodoEnforcer(session_id)
        return self.current_todo
    
    def get_todo(self) -> TodoEnforcer:
        """获取当前 todo"""
        if not self.current_todo:
            self.current_todo = self.create_todo_session()
        return self.current_todo
    
    # ============ Category Routing ============
    
    def get_category_info(self, category: str) -> dict:
        """获取 category 信息"""
        return self.categories.get(category, {})
    
    def get_agent_for_category(self, category: str) -> str:
        """获取 category 对应的 agent"""
        cat_info = self.get_category_info(category)
        agents = cat_info.get("agents", ["hephaestus"])
        return agents[0] if agents else "hephaestus"
    
    def route_task(self, prompt: str) -> dict:
        """路由任务（意图分析 + category 映射）"""
        # 1. 分析意图
        intent_result = self.analyze_intent(prompt)
        
        # 2. 获取 category 信息
        category = intent_result["category"]
        cat_info = self.get_category_info(category)
        
        # 3. 确定 agent
        agent = self.get_agent_for_category(category)
        
        return {
            "prompt": prompt,
            "intent": intent_result["intent"],
            "category": category,
            "complexity": intent_result["complexity"],
            "confidence": intent_result["confidence"],
            "model": cat_info.get("default_model", "xiaomi/MiniMax-M2.5"),
            "agent": agent,
            "reasoning": intent_result["reasoning"]
        }
    
    # ============ Parallel Scheduler ============
    
    def create_scheduler(self, max_parallel: int = 5) -> ParallelScheduler:
        """创建并行调度器"""
        self.current_scheduler = ParallelScheduler(max_parallel)
        return self.current_scheduler
    
    # ============ Wisdom ============
    
    def create_notepad(self, plan_name: str):
        """创建学习笔记本"""
        return self.wisdom.create_notepad(plan_name)
    
    # ============ 工具函数 ============
    
    def list_agents(self) -> list:
        """列出所有 agents"""
        return [
            {"name": name, **info}
            for name, info in self.agents.items()
        ]
    
    def list_categories(self) -> list:
        """列出所有 categories"""
        return [
            {"name": name, **info}
            for name, info in self.categories.items()
        ]
    
    def get_system_status(self) -> dict:
        """获取系统状态"""
        return {
            "agents_count": len(self.agents),
            "categories_count": len(self.categories),
            "has_todo_session": self.current_todo is not None,
            "has_scheduler": self.current_scheduler is not None,
            "notepads": self.wisdom.list_notepads()
        }
    
    def generate_system_prompt(self, mode: str = "sisyphus") -> str:
        """生成系统 prompt"""
        prompts_dir = self.workspace_dir / "prompts"
        prompt_file = prompts_dir / f"{mode}.md"
        
        if prompt_file.exists():
            with open(prompt_file) as f:
                return f.read()
        
        return f"# {mode.title()}\n\n你是 {mode} agent。"


# CLI 入口
def main():
    omo = OMOSystem()
    
    if len(sys.argv) < 2:
        print("OMO - OpenClaw Multi-Agent Orchestration")
        print("\nCommands:")
        print("  status                    - System status")
        print("  list-agents               - List all agents")
        print("  list-categories           - List all categories")
        print("  route <prompt>            - Route task by prompt")
        print("  intent <prompt>           - Analyze intent")
        print("  prompt <agent>            - Get agent prompt")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        print(json.dumps(omo.get_system_status(), indent=2, ensure_ascii=False))
    
    elif cmd == "list-agents":
        for a in omo.list_agents():
            print(f"  {a['name']:20} - {a.get('role', '')}")
    
    elif cmd == "list-categories":
        for c in omo.list_categories():
            print(f"  {c['name']:20} - {c.get('description', '')}")
    
    elif cmd == "route":
        if len(sys.argv) < 3:
            print("Usage: omo.py route <prompt>")
            sys.exit(1)
        result = omo.route_task(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "intent":
        if len(sys.argv) < 3:
            print("Usage: omo.py intent <prompt>")
            sys.exit(1)
        result = omo.analyze_intent(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "prompt":
        if len(sys.argv) < 3:
            print("Usage: omo.py prompt <agent>")
            sys.exit(1)
        print(omo.generate_system_prompt(sys.argv[2]))
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
