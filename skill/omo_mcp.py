#!/usr/bin/env python3
"""
OMO MCP Server - 让 OpenClaw 可以调用 OMO 功能
"""

import json
import sys
from omo import OMOSystem

# 初始化 OMO 系统
omo = OMOSystem()

def handle_request(request):
    """处理 MCP 请求"""
    method = request.get("method")
    params = request.get("params", {})
    
    try:
        if method == "route_task":
            prompt = params.get("prompt", "")
            result = omo.route_task(prompt)
            return {"ok": True, "result": result}
        
        elif method == "analyze_intent":
            prompt = params.get("prompt", "")
            result = omo.analyze_intent(prompt)
            return {"ok": True, "result": result}
        
        elif method == "list_agents":
            return {"ok": True, "result": omo.list_agents()}
        
        elif method == "list_categories":
            return {"ok": True, "result": omo.list_categories()}
        
        elif method == "get_system_status":
            return {"ok": True, "result": omo.get_system_status()}
        
        elif method == "create_todo_session":
            session_id = params.get("session_id", "default")
            todo = omo.create_todo_session(session_id)
            return {"ok": True, "result": {"session_id": session_id}}
        
        elif method == "add_todo":
            todo = omo.get_todo()
            content = params.get("content", "")
            priority = params.get("priority", "normal")
            item = todo.add(content, priority)
            return {"ok": True, "result": item.to_dict()}
        
        elif method == "complete_todo":
            todo = omo.get_todo()
            content = params.get("content")
            item = todo.complete(content)
            if item:
                return {"ok": True, "result": item.to_dict()}
            return {"ok": False, "error": "No todo to complete"}
        
        elif method == "get_todo_status":
            todo = omo.get_todo()
            return {
                "ok": True,
                "result": {
                    "pending": len(todo.get_pending()),
                    "completed": todo.get_completed_count(),
                    "total": todo.get_total_count(),
                    "is_all_completed": todo.is_all_completed(),
                    "markdown": todo.to_markdown()
                }
            }
        
        elif method == "check_todo_reminder":
            todo = omo.get_todo()
            reminder = todo.check_and_remind()
            if reminder:
                return {"ok": True, "result": {"has_reminder": True, "message": reminder}}
            return {"ok": True, "result": {"has_reminder": False}}
        
        elif method == "get_agent_prompt":
            agent = params.get("agent", "sisyphus")
            prompt = omo.generate_system_prompt(agent)
            return {"ok": True, "result": {"agent": agent, "prompt": prompt}}
        
        else:
            return {"ok": False, "error": f"Unknown method: {method}"}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}


# MCP 协议处理
if __name__ == "__main__":
    # 读取 stdin 的 JSON-RPC 请求
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"ok": False, "error": "Invalid JSON"}), flush=True)
        except Exception as e:
            print(json.dumps({"ok": False, "error": str(e)}), flush=True)
