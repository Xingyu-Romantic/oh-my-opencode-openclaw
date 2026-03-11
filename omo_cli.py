#!/usr/bin/env python3
"""
OMO (Oh My OpenClaw) - Agent Orchestration System
参考: https://github.com/code-yeongyu/oh-my-openagent
"""

import json
import yaml
import os
from pathlib import Path

OMO_DIR = Path(__file__).parent
AGENTS_CONFIG = OMO_DIR / "agents.yaml"
CATEGORIES_CONFIG = OMO_DIR / "categories.yaml"

def load_config():
    """加载配置"""
    with open(AGENTS_CONFIG) as f:
        agents = yaml.safe_load(f)['agents']
    with open(CATEGORIES_CONFIG) as f:
        categories = yaml.safe_load(f)['categories']
    return agents, categories

def get_agent_info(agent_name: str):
    """获取 agent 信息"""
    agents, _ = load_config()
    if agent_name not in agents:
        return None
    return agents[agent_name]

def get_category_info(category: str):
    """获取 category 信息"""
    _, categories = load_config()
    if category not in categories:
        return None
    return categories[category]

def route_task(category: str, prompt: str):
    """根据 category 路由任务"""
    cat_info = get_category_info(category)
    if not cat_info:
        return {"error": f"Unknown category: {category}"}
    
    # 返回路由信息
    return {
        "category": category,
        "description": cat_info['description'],
        "model": cat_info['default_model'],
        "fallback_chain": cat_info['fallback_chain'],
        "available_agents": cat_info['agents'],
        "prompt": prompt
    }

def list_agents():
    """列出所有 agents"""
    agents, _ = load_config()
    return [
        {
            "name": name,
            "role": info["role"],
            "description": info["description"],
            "model": info["model"]
        }
        for name, info in agents.items()
    ]

def list_categories():
    """列出所有 categories"""
    _, categories = load_config()
    return [
        {
            "name": name,
            "description": info["description"],
            "model": info["default_model"]
        }
        for name, info in categories.items()
    ]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: omo_cli.py <command> [args]")
        print("\nCommands:")
        print("  list-agents              - List all agents")
        print("  list-categories          - List all categories")
        print("  route <category> <prompt> - Route task by category")
        print("  agent <name>             - Show agent info")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list-agents":
        for a in list_agents():
            print(f"  {a['name']:20} - {a['role']}: {a['model']}")
    
    elif cmd == "list-categories":
        for c in list_categories():
            print(f"  {c['name']:20} - {c['description']}: {c['model']}")
    
    elif cmd == "route":
        if len(sys.argv) < 4:
            print("Usage: omo_cli.py route <category> <prompt>")
            sys.exit(1)
        result = route_task(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "agent":
        if len(sys.argv) < 3:
            print("Usage: omo_cli.py agent <name>")
            sys.exit(1)
        info = get_agent_info(sys.argv[2])
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print(f"Agent not found: {sys.argv[2]}")
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
