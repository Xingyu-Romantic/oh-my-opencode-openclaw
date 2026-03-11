#!/usr/bin/env python3
"""
Wisdom Accumulator - 经验累积系统
跨任务累积学习，让下一个任务更聪明
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class WisdomEntry:
    """经验条目"""
    def __init__(self, category: str, content: str, source_task: str = ""):
        self.category = category  # conventions, successes, failures, gotchas, commands
        self.content = content
        self.source_task = source_task
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "category": self.category,
            "content": self.content,
            "source_task": self.source_task,
            "created_at": self.created_at
        }


class Notepad:
    """学习笔记本"""
    
    CATEGORIES = [
        "learnings",      # 成功的模式、约定
        "decisions",      # 架构决策和理由
        "issues",         # 遇到的问题、阻塞、坑
        "verification",   # 测试结果、验证结果
        "problems"        # 未解决的问题、技术债务
    ]
    
    def __init__(self, plan_name: str, base_dir: str = None):
        self.plan_name = plan_name
        self.base_dir = Path(base_dir) if base_dir else Path("omo-system/notepads")
        self.notepad_dir = self.base_dir / plan_name
        self.entries: Dict[str, List[WisdomEntry]] = {cat: [] for cat in self.CATEGORIES + ["gotchas"]}
        
        # 创建目录
        self.notepad_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载现有数据
        self._load()
    
    def _load(self):
        """加载现有数据"""
        for category in self.CATEGORIES:
            file_path = self.notepad_dir / f"{category}.md"
            if file_path.exists():
                with open(file_path) as f:
                    content = f.read()
                    # 解析现有内容
                    self.entries[category] = self._parse_content(category, content)
    
    def _parse_content(self, category: str, content: str) -> List[WisdomEntry]:
        """解析内容为条目"""
        entries = []
        lines = content.split("\n")
        current_entry = []
        
        for line in lines:
            if line.startswith("### ") and current_entry:
                # 保存前一个
                entries.append(WisdomEntry(category, "\n".join(current_entry)))
                current_entry = []
            current_entry.append(line)
        
        if current_entry:
            entries.append(WisdomEntry(category, "\n".join(current_entry)))
        
        return entries
    
    def add(self, category: str, content: str, source_task: str = ""):
        """添加经验"""
        if category not in self.CATEGORIES:
            category = "learnings"  # 默认
        
        entry = WisdomEntry(category, content, source_task)
        self.entries[category].append(entry)
        
        # 保存到文件
        self._save(category)
        
        return entry
    
    def _save(self, category: str):
        """保存到文件"""
        file_path = self.notepad_dir / f"{category}.md"
        
        with open(file_path, "w") as f:
            f.write(f"# {category.title()}\n\n")
            f.write(f"_Generated at {datetime.now().isoformat()}_\n\n")
            
            for entry in self.entries[category]:
                f.write(f"### \n")
                f.write(entry.content)
                f.write("\n\n---\n\n")
    
    def get_all(self) -> Dict[str, List[WisdomEntry]]:
        """获取所有经验"""
        return self.entries
    
    def get_for_context(self) -> str:
        """获取上下文格式的经验"""
        context_parts = []
        
        # Learnings
        if self.entries["learnings"]:
            context_parts.append("### 成功模式 (Learnings)\n")
            for e in self.entries["learnings"]:
                context_parts.append(f"- {e.content.split(chr(10))[0]}")
        
        # Issues (警告)
        if self.entries["issues"]:
            context_parts.append("\n### 已知问题 (Issues)\n")
            for e in self.entries["issues"]:
                context_parts.append(f"- ⚠️ {e.content.split(chr(10))[0]}")
        
        # Gotchas (坑)
        if self.entries["gotchas"]:
            context_parts.append("\n### 已踩坑 (Gotchas)\n")
            for e in self.entries["gotchas"]:
                context_parts.append(f"- 🔴 {e.content.split(chr(10))[0]}")
        
        return "\n".join(context_parts) if context_parts else "_暂无经验_"
    
    def summarize(self) -> str:
        """生成摘要"""
        lines = [f"# 📓 学习笔记本: {self.plan_name}", ""]
        
        for category in self.CATEGORIES:
            count = len(self.entries[category])
            if count > 0:
                lines.append(f"- **{category.title()}**: {count} 条")
        
        return "\n".join(lines)


class WisdomAccumulator:
    """经验累积器"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path("omo-system/notepads")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.current_notepad: Optional[Notepad] = None
    
    def create_notepad(self, plan_name: str) -> Notepad:
        """创建新的笔记本"""
        self.current_notepad = Notepad(plan_name, str(self.base_dir))
        return self.current_notepad
    
    def get_notepad(self, plan_name: str) -> Notepad:
        """获取笔记本"""
        return Notepad(plan_name, str(self.base_dir))
    
    def add_learnings(self, content: str, source_task: str = ""):
        """添加成功经验"""
        if self.current_notepad:
            self.current_notepad.add("learnings", content, source_task)
    
    def add_issue(self, content: str, source_task: str = ""):
        """添加问题"""
        if self.current_notepad:
            self.current_notepad.add("issues", content, source_task)
    
    def add_decision(self, content: str, source_task: str = ""):
        """添加决策"""
        if self.current_notepad:
            self.current_notepad.add("decisions", content, source_task)
    
    def add_problem(self, content: str, source_task: str = ""):
        """添加未解决问题"""
        if self.current_notepad:
            self.current_notepad.add("problems", content, source_task)
    
    def get_context_for_next_task(self) -> str:
        """获取传递给下一个任务的上下文"""
        if self.current_notepad:
            return self.current_notepad.get_for_context()
        return ""
    
    def list_notepads(self) -> List[str]:
        """列出所有笔记本"""
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]


# 测试
if __name__ == "__main__":
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        acc = WisdomAccumulator(tmpdir)
        
        # 创建笔记本
        np = acc.create_notepad("user-login-feature")
        
        # 添加经验
        np.add("learnings", "使用 bcrypt 加密密码，不要用 md5")
        np.add("learnings", "用户表需要 email 唯一索引")
        np.add("issues", "旧代码没有处理并发登录问题")
        np.add("decisions", "使用 JWT 做 token 认证")
        
        # 打印摘要
        print(np.summarize())
        print("\n" + "="*50 + "\n")
        
        # 获取上下文
        print("传递给下一个任务的上下文:")
        print(acc.get_context_for_next_task())
