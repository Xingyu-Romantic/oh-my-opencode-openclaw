#!/usr/bin/env python3
"""
Todo Enforcer - 强制完成机制
确保 Agent 不摸鱼，所有任务都必须完成
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime

class TodoItem:
    """Todo 项"""
    def __init__(self, content: str, status: str = "pending", priority: str = "normal"):
        self.content = content
        self.status = status  # pending, in_progress, completed
        self.priority = priority  # low, normal, high, critical
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def to_dict(self):
        return {
            "content": self.content,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @staticmethod
    def from_dict(data):
        item = TodoItem(data["content"], data["status"], data["priority"])
        item.created_at = data.get("created_at", datetime.now().isoformat())
        item.completed_at = data.get("completed_at")
        return item


class TodoEnforcer:
    """Todo 强制器"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.todos: List[TodoItem] = []
        self.reminder_count = 0
        self.max_reminders = 10
    
    def add(self, content: str, priority: str = "normal") -> TodoItem:
        """添加 todo"""
        todo = TodoItem(content, "pending", priority)
        self.todos.append(todo)
        return todo
    
    def add_many(self, items: List[str], priority: str = "normal"):
        """批量添加 todos"""
        return [self.add(item, priority) for item in items]
    
    def start(self, content: str = None) -> Optional[TodoItem]:
        """开始一个 todo"""
        # 找到第一个 pending 的
        for todo in self.todos:
            if todo.status == "pending":
                todo.status = "in_progress"
                return todo
        
        # 如果指定了 content，查找或创建
        if content:
            for todo in self.todos:
                if content in todo.content and todo.status != "completed":
                    todo.status = "in_progress"
                    return todo
            # 没找到，创建新的
            return self.add(content, "high")
        
        return None
    
    def complete(self, content: str = None) -> Optional[TodoItem]:
        """完成一个 todo"""
        # 找到第一个 in_progress 的
        for todo in self.todos:
            if todo.status == "in_progress":
                todo.status = "completed"
                todo.completed_at = datetime.now().isoformat()
                return todo
        
        # 如果指定了 content，查找并完成
        if content:
            for todo in self.todos:
                if content in todo.content and todo.status != "completed":
                    todo.status = "completed"
                    todo.completed_at = datetime.now().isoformat()
                    return todo
        
        return None
    
    def get_pending(self) -> List[TodoItem]:
        """获取所有 pending 的 todos"""
        return [t for t in self.todos if t.status != "completed"]
    
    def get_in_progress(self) -> Optional[TodoItem]:
        """获取当前进行中的 todo"""
        for t in self.todos:
            if t.status == "in_progress":
                return t
        return None
    
    def get_completed_count(self) -> int:
        """获取完成数量"""
        return sum(1 for t in self.todos if t.status == "completed")
    
    def get_total_count(self) -> int:
        """获取总数量"""
        return len(self.todos)
    
    def is_all_completed(self) -> bool:
        """是否全部完成"""
        return len(self.todos) > 0 and all(t.status == "completed" for t in self.todos)
    
    def generate_reminder(self) -> str:
        """生成强制提醒"""
        self.reminder_count += 1
        
        pending = self.get_pending()
        in_progress = self.get_in_progress()
        
        reminder = f"""
[🚨 系统提醒 - TODO 强制继续]

你有未完成的 todos！完成所有后再回复。

"""
        
        if in_progress:
            reminder += f"▸ 当前进行中: {in_progress.content}\n\n"
        
        reminder += "待完成:\n"
        for i, todo in enumerate(pending, 1):
            status_icon = "⏳" if todo.status == "pending" else "🔄"
            priority_mark = "🔴" if todo.priority == "critical" else "🟡" if todo.priority == "high" else "  "
            reminder += f"{priority_mark} {status_icon} [{i}] {todo.content}\n"
        
        reminder += f"""
---
进度: {self.get_completed_count()}/{self.get_total_count()}
提醒次数: {self.reminder_count}/{self.max_reminders}

⚠️ 未完成所有 todos 前不要回复！
"""
        return reminder
    
    def check_and_remind(self) -> Optional[str]:
        """检查并返回提醒（如果有未完成的 todo）"""
        if self.is_all_completed():
            return None
        
        if self.reminder_count >= self.max_reminders:
            return f"[⚠️ 警告] 已达到最大提醒次数 ({self.max_reminders})，任务仍未完成。"
        
        return self.generate_reminder()
    
    def parse_from_text(self, text: str):
        """从文本解析 todos"""
        # 匹配 - [ ] 或 - [x] 格式
        pattern = r'-\s*\[([ x])\]\s*(.+?)(?:\s*←|$)'
        matches = re.findall(pattern, text, re.MULTILINE)
        
        for checked, content in matches:
            status = "completed" if checked == "x" else "pending"
            # 检查是否已存在
            exists = any(content.strip() in t.content for t in self.todos)
            if not exists:
                todo = TodoItem(content.strip(), status)
                self.todos.append(todo)
        
        return len(matches)
    
    def to_markdown(self) -> str:
        """转换为 markdown 格式"""
        if not self.todos:
            return "## Todos\n\n_暂无任务_"
        
        lines = ["## Todos", ""]
        
        # 进行中的
        in_progress = self.get_in_progress()
        if in_progress:
            lines.append(f"▸ **{in_progress.content}** ← 进行中")
            lines.append("")
        
        # Pending
        pending = [t for t in self.todos if t.status == "pending"]
        if pending:
            lines.append("### 待完成")
            for todo in pending:
                priority = "🔴" if todo.priority == "critical" else "🟡" if todo.priority == "high" else "  "
                lines.append(f"- [ ] {priority} {todo.content}")
            lines.append("")
        
        # Completed
        completed = [t for t in self.todos if t.status == "completed"]
        if completed:
            lines.append("### 已完成")
            for todo in completed:
                lines.append(f"- [x] ~~{todo.content}~~")
        
        lines.append("")
        lines.append(f"**进度**: {self.get_completed_count()}/{self.get_total_count()}")
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """序列化为 JSON"""
        return json.dumps({
            "session_id": self.session_id,
            "todos": [t.to_dict() for t in self.todos],
            "progress": {
                "completed": self.get_completed_count(),
                "total": self.get_total_count()
            }
        }, indent=2, ensure_ascii=False)
    
    @staticmethod
    def from_json(json_str: str) -> 'TodoEnforcer':
        """从 JSON 反序列化"""
        data = json.loads(json_str)
        enforcer = TodoEnforcer(data.get("session_id", "default"))
        enforcer.todos = [TodoItem.from_dict(t) for t in data.get("todos", [])]
        return enforcer


# 测试
if __name__ == "__main__":
    enforcer = TodoEnforcer("test-session")
    
    # 添加 todos
    enforcer.add_many([
        "实现用户服务",
        "添加验证逻辑",
        "编写单元测试",
        "更新 API 文档"
    ], "normal")
    
    # 开始第一个
    enforcer.start()
    
    # 打印状态
    print(enforcer.to_markdown())
    print("\n" + "="*50 + "\n")
    
    # 完成第一个
    enforcer.complete()
    
    # 检查提醒
    reminder = enforcer.check_and_remind()
    if reminder:
        print(reminder)
