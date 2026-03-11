#!/usr/bin/env python3
"""
Parallel Task Scheduler - 并行任务调度器
同时启动多个 agent 工作
"""

import asyncio
import json
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """任务"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    prompt: str = ""
    category: str = "unspecified-low"
    agent: str = "hephaestus"
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str = ""
    completed_at: str = ""
    dependencies: List[str] = field(default_factory=list)  # 依赖的任务 ID
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "prompt": self.prompt[:100] + "..." if len(self.prompt) > 100 else self.prompt,
            "category": self.category,
            "agent": self.agent,
            "status": self.status.value,
            "result": str(self.result)[:200] if self.result else None,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "dependencies": self.dependencies
        }


class ParallelScheduler:
    """并行任务调度器"""
    
    def __init__(self, max_parallel: int = 5):
        self.max_parallel = max_parallel
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: List[str] = []
        self.completed_tasks: List[str] = []
        self.failed_tasks: List[str] = []
        
        # 执行器函数 (由外部注入)
        self.executor: Optional[Callable] = None
    
    def set_executor(self, executor: Callable):
        """设置执行器函数"""
        self.executor = executor
    
    def add_task(self, name: str, prompt: str, category: str = "unspecified-low", 
                 agent: str = "hephaestus", dependencies: List[str] = None) -> Task:
        """添加任务"""
        task = Task(
            name=name,
            prompt=prompt,
            category=category,
            agent=agent,
            dependencies=dependencies or []
        )
        self.tasks[task.id] = task
        return task
    
    def add_tasks(self, task_specs: List[Dict]) -> List[Task]:
        """批量添加任务"""
        tasks = []
        for spec in task_specs:
            task = self.add_task(
                name=spec.get("name", ""),
                prompt=spec.get("prompt", ""),
                category=spec.get("category", "unspecified-low"),
                agent=spec.get("agent", "hephaestus"),
                dependencies=spec.get("dependencies", [])
            )
            tasks.append(task)
        return tasks
    
    def can_run(self, task: Task) -> bool:
        """检查任务是否可以运行"""
        if task.status != TaskStatus.PENDING:
            return False
        
        # 检查依赖是否都完成
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        return True
    
    def get_ready_tasks(self) -> List[Task]:
        """获取就绪的任务"""
        ready = []
        for task in self.tasks.values():
            if self.can_run(task) and len(self.running_tasks) < self.max_parallel:
                ready.append(task)
        return ready
    
    async def run_task(self, task: Task) -> Task:
        """运行单个任务"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        self.running_tasks.append(task.id)
        
        try:
            if self.executor:
                # 调用外部执行器
                result = await self.executor(task)
                task.result = result
                task.status = TaskStatus.COMPLETED
                self.completed_tasks.append(task.id)
            else:
                # 没有执行器，模拟运行
                await asyncio.sleep(0.1)
                task.result = f"Simulated result for {task.name}"
                task.status = TaskStatus.COMPLETED
                self.completed_tasks.append(task.id)
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.failed_tasks.append(task.id)
        finally:
            task.completed_at = datetime.now().isoformat()
            if task.id in self.running_tasks:
                self.running_tasks.remove(task.id)
        
        return task
    
    async def run_all(self) -> List[Task]:
        """运行所有任务"""
        while True:
            # 获取就绪任务
            ready_tasks = self.get_ready_tasks()
            
            if not ready_tasks and not self.running_tasks:
                # 没有更多任务可运行
                break
            
            # 运行就绪的任务
            if ready_tasks:
                await asyncio.gather(*[self.run_task(t) for t in ready_tasks])
            
            # 如果没有就绪任务但有运行中的任务，等待
            if not ready_tasks and self.running_tasks:
                await asyncio.sleep(0.1)
        
        return list(self.tasks.values())
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "total": len(self.tasks),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "running": len(self.running_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "max_parallel": self.max_parallel
        }
    
    def get_results(self) -> List[Dict]:
        """获取所有结果"""
        return [t.to_dict() for t in self.tasks.values()]
    
    def get_failed_tasks(self) -> List[Task]:
        """获取失败的任务"""
        return [self.tasks[tid] for tid in self.failed_tasks]
    
    def to_markdown(self) -> str:
        """转换为 markdown"""
        lines = ["## 📋 任务执行状态", ""]
        
        status = self.get_status()
        lines.append(f"**总任务数**: {status['total']}")
        lines.append(f"**待处理**: {status['pending']} | **运行中**: {status['running']} | **完成**: {status['completed']} | **失败**: {status['failed']}")
        lines.append("")
        
        # 按状态分组
        for task in self.tasks.values():
            icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.RUNNING: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.CANCELLED: "🚫"
            }.get(task.status, "❓")
            
            status_text = f"{icon} {task.status.value}"
            if task.status == TaskStatus.FAILED:
                status_text += f" - {task.error[:50]}"
            
            lines.append(f"- **{task.name}** ({task.agent}, {task.category})")
            lines.append(f"  - {status_text}")
        
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    async def mock_executor(task: Task):
        """模拟执行器"""
        await asyncio.sleep(0.2)
        return f"Result of {task.name}"
    
    async def main():
        scheduler = ParallelScheduler(max_parallel=3)
        scheduler.set_executor(mock_executor)
        
        # 添加任务
        scheduler.add_tasks([
            {"name": "探索代码库", "prompt": "了解项目结构", "category": "quick", "agent": "explore"},
            {"name": "实现用户服务", "prompt": "创建用户 CRUD", "category": "deep", "agent": "hephaestus"},
            {"name": "添加验证", "prompt": "输入验证逻辑", "category": "quick", "agent": "hephaestus"},
            {"name": "编写测试", "prompt": "单元测试", "category": "quick", "agent": "hephaestus"},
            {"name": "更新文档", "prompt": "API 文档", "category": "writing", "agent": "librarian"},
        ])
        
        print("开始执行任务...")
        results = await scheduler.run_all()
        
        print("\n" + scheduler.to_markdown())
        
        print("\n失败的任务:")
        for t in scheduler.get_failed_tasks():
            print(f"  - {t.name}: {t.error}")
    
    asyncio.run(main())
