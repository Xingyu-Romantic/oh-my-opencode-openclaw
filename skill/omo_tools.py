#!/usr/bin/env python3
"""
OMO Tools for OpenClaw
提供可以被 OpenClaw 调用的工具函数
"""

import json
import sys
import os
from pathlib import Path

# 添加当前目录到路径
OMO_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OMO_PATH)

from omo import OMOSystem

# 全局 OMO 实例
_omo = None

def get_omo():
    """获取 OMO 实例"""
    global _omo
    if _omo is None:
        _omo = OMOSystem()
    return _omo

def route_task(prompt: str) -> dict:
    """
    路由任务 - 分析意图并返回合适的 agent 和 category
    
    Args:
        prompt: 用户任务描述
        
    Returns:
        dict: 包含 intent, category, agent, model 等信息
    """
    omo = get_omo()
    return omo.route_task(prompt)

def analyze_intent(prompt: str) -> dict:
    """
    意图分析 - 只分析意图，不路由
    
    Args:
        prompt: 用户任务描述
        
    Returns:
        dict: 包含 intent, category, complexity, confidence 等信息
    """
    omo = get_omo()
    return omo.analyze_intent(prompt)

def list_agents() -> list:
    """列出所有 agents"""
    omo = get_omo()
    return omo.list_agents()

def list_categories() -> list:
    """列出所有 categories"""
    omo = get_omo()
    return omo.list_categories()

def get_agent_prompt(agent: str) -> str:
    """获取 agent 的系统 prompt"""
    omo = get_omo()
    return omo.generate_system_prompt(agent)

def get_system_status() -> dict:
    """获取系统状态"""
    omo = get_omo()
    return omo.get_system_status()

# CLI 入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: omo_tools.py <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "route":
        if len(sys.argv) < 3:
            print("Usage: omo_tools.py route <prompt>")
            sys.exit(1)
        result = route_task(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "intent":
        if len(sys.argv) < 3:
            print("Usage: omo_tools.py intent <prompt>")
            sys.exit(1)
        result = analyze_intent(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "list-agents":
        result = list_agents()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "list-categories":
        result = list_categories()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "prompt":
        if len(sys.argv) < 3:
            print("Usage: omo_tools.py prompt <agent>")
            sys.exit(1)
        result = get_agent_prompt(sys.argv[2])
        print(result)
    
    elif cmd == "status":
        result = get_system_status()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
