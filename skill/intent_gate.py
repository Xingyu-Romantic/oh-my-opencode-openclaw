#!/usr/bin/env python3
"""
Intent Gate - 意图分析系统
分析用户真实意图，分类任务类型
"""

import re
from enum import Enum
from typing import Dict, List, Optional

class IntentType(Enum):
    """意图类型"""
    RESEARCH = "research"        # 研究/调研
    IMPLEMENTATION = "implementation"  # 实现/开发
    INVESTIGATION = "investigation"  # 调查/排查
    FIX = "fix"                  # 修复 bug
    REFACTORING = "refactoring"  # 重构
    BUILD_SCRATCH = "build_from_scratch"  # 从零构建
    ARCHITECTURE = "architecture"  # 架构决策
    QUICK = "quick"              # 简单快速任务
    UNKNOWN = "unknown"          # 未知

# 意图关键词映射
INTENT_PATTERNS = {
    IntentType.RESEARCH: [
        r"研究", r"调研", r"调查", r"了解", r"看看", r"搜索", r"查找",
        r"research", r"investigate", r"explore", r"find", r"search"
    ],
    IntentType.IMPLEMENTATION: [
        r"实现", r"开发", r"添加", r"创建", r"构建", r"写",
        r"implement", r"develop", r"add", r"create", r"build", r"make"
    ],
    IntentType.INVESTIGATION: [
        r"为什么", r"怎么回事", r"什么情况", r"调查", r"排查",
        r"why", r"what.*wrong", r"debug", r"investigate"
    ],
    IntentType.FIX: [
        r"修复", r"解决", r"bug", r"错误", r"问题", r"报错",
        r"fix", r"repair", r"resolve", r"issue", r"error", r"problem"
    ],
    IntentType.REFACTORING: [
        r"重构", r"优化", r"整理", r"重写",
        r"refactor", r"optimize", r"improve", r"restructure"
    ],
    IntentType.BUILD_SCRATCH: [
        r"从零", r"新建", r"全新", r"白手起家",
        r"from scratch", r"new project", r"brand new", r"create new"
    ],
    IntentType.ARCHITECTURE: [
        r"架构", r"设计", r"方案", r"选型",
        r"architecture", r"design", r"structure", r"pattern"
    ],
    IntentType.QUICK: [
        r"简单", r"快速", r"小改", r" typo", r"拼写",
        r"simple", r"quick", r"small", r"typo", r"fix typo"
    ],
}

# 意图到 Category 的映射
INTENT_TO_CATEGORY = {
    IntentType.RESEARCH: "unspecified-low",
    IntentType.IMPLEMENTATION: "unspecified-high",
    IntentType.INVESTIGATION: "deep",
    IntentType.FIX: "quick",
    IntentType.REFACTORING: "deep",
    IntentType.BUILD_SCRATCH: "unspecified-high",
    IntentType.ARCHITECTURE: "ultrabrain",
    IntentType.QUICK: "quick",
    IntentType.UNKNOWN: "unspecified-low",
}

# 复杂度关键词
COMPLEXITY_INDICATORS = {
    "high": [
        r"复杂", r"大型", r"多个", r"重构", r"系统",
        r"complex", r"large", r"multiple", r"system", r"architecture"
    ],
    "low": [
        r"简单", r"单个", r"小", r"一个",
        r"simple", r"single", r"small", r"one"
    ]
}

class IntentGate:
    """意图分析门"""
    
    def __init__(self):
        self.patterns = INTENT_PATTERNS
        self.complexity_indicators = COMPLEXITY_INDICATORS
    
    def analyze(self, prompt: str) -> Dict:
        """
        分析用户意图
        返回: {
            "intent": IntentType,
            "category": str,
            "complexity": "high" | "low" | "medium",
            "confidence": float,
            "reasoning": str
        }
        """
        prompt_lower = prompt.lower()
        
        # 1. 检测意图类型
        intent = self._detect_intent(prompt_lower)
        
        # 2. 检测复杂度
        complexity = self._detect_complexity(prompt_lower)
        
        # 3. 确定 category
        category = INTENT_TO_CATEGORY.get(intent, "unspecified-low")
        
        # 4. 如果复杂度高，提升 category
        if complexity == "high" and category == "unspecified-low":
            category = "unspecified-high"
        
        # 5. 计算置信度
        confidence = self._calculate_confidence(prompt_lower, intent)
        
        return {
            "intent": intent.value,
            "category": category,
            "complexity": complexity,
            "confidence": confidence,
            "reasoning": self._generate_reasoning(intent, complexity, category)
        }
    
    def _detect_intent(self, prompt: str) -> IntentType:
        """检测意图类型"""
        scores = {}
        
        for intent_type, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, prompt):
                    score += 1
            if score > 0:
                scores[intent_type] = score
        
        if not scores:
            return IntentType.UNKNOWN
        
        # 返回得分最高的意图
        return max(scores, key=scores.get)
    
    def _detect_complexity(self, prompt: str) -> str:
        """检测复杂度"""
        high_count = sum(1 for p in self.complexity_indicators["high"] 
                        if re.search(p, prompt))
        low_count = sum(1 for p in self.complexity_indicators["low"] 
                       if re.search(p, prompt))
        
        if high_count > low_count:
            return "high"
        elif low_count > high_count:
            return "low"
        return "medium"
    
    def _calculate_confidence(self, prompt: str, intent: IntentType) -> float:
        """计算置信度"""
        patterns = self.patterns.get(intent, [])
        matches = sum(1 for p in patterns if re.search(p, prompt))
        
        if not patterns:
            return 0.5
        
        return min(matches / len(patterns) + 0.5, 1.0)
    
    def _generate_reasoning(self, intent: IntentType, complexity: str, category: str) -> str:
        """生成推理说明"""
        return f"检测到意图: {intent.value}, 复杂度: {complexity}, 路由到: {category}"


# 测试
if __name__ == "__main__":
    gate = IntentGate()
    
    test_prompts = [
        "实现一个用户登录功能",
        "修复登录页面的 bug",
        "帮我看看这个错误怎么回事",
        "重构用户模块的代码",
        "研究一下这个库的用法",
        "设计一个分布式系统架构",
        "改个 typo",
    ]
    
    for p in test_prompts:
        result = gate.analyze(p)
        print(f"\n📝 {p}")
        print(f"   → 意图: {result['intent']}, 复杂度: {result['complexity']}")
        print(f"   → Category: {result['category']}, 置信度: {result['confidence']:.2f}")
