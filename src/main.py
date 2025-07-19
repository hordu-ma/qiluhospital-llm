# 智能体开发主代码文件

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class PromptType(Enum):
    """提示词类型枚举"""
    CREATIVE = "creative"  # 创意生成
    ANALYTICAL = "analytical"  # 分析型
    CONVERSATIONAL = "conversational"  # 对话型
    INSTRUCTIONAL = "instructional"  # 指令型

@dataclass
class PromptStructure:
    """标准提示词结构"""
    role: str  # 角色设定
    task: str  # 具体任务
    context: str  # 上下文信息
    requirements: List[str]  # 具体要求
    format: str  # 输出格式
    examples: List[str]  # 示例
    constraints: List[str]  # 约束条件
    tone: str  # 语调风格
    prompt_type: str  # 提示词类型

class PromptOptimizer:
    """提示词优化器"""
    
    def __init__(self):
        self.role_keywords = {
            "专家": "expert", "助手": "assistant", "老师": "teacher", 
            "分析师": "analyst", "顾问": "consultant", "作家": "writer"
        }
        
        self.task_patterns = [
            r"帮我(.*?)(?:，|。|$)",
            r"请(.*?)(?:，|。|$)",
            r"需要(.*?)(?:，|。|$)",
            r"想要(.*?)(?:，|。|$)"
        ]
        
        self.format_keywords = {
            "列表": "list", "表格": "table", "段落": "paragraph",
            "要点": "bullet_points", "代码": "code", "报告": "report"
        }
        
        self.tone_keywords = {
            "专业": "professional", "友好": "friendly", "正式": "formal",
            "幽默": "humorous", "简洁": "concise", "详细": "detailed"
        }

    def analyze_natural_prompt(self, prompt: str) -> Dict:
        """分析自然语言提示词"""
        analysis = {
            "role": self._extract_role(prompt),
            "task": self._extract_task(prompt),
            "context": self._extract_context(prompt),
            "requirements": self._extract_requirements(prompt),
            "format": self._extract_format(prompt),
            "tone": self._extract_tone(prompt),
            "prompt_type": self._classify_prompt_type(prompt)
        }
        return analysis

    def _extract_role(self, prompt: str) -> str:
        """提取角色信息"""
        for keyword, role in self.role_keywords.items():
            if keyword in prompt:
                return f"你是一位{keyword}"
        return "你是一位AI助手"

    def _extract_task(self, prompt: str) -> str:
        """提取任务信息"""
        for pattern in self.task_patterns:
            match = re.search(pattern, prompt)
            if match:
                return match.group(1).strip()
        return prompt.split("。")[0] if "。" in prompt else prompt

    def _extract_context(self, prompt: str) -> str:
        """提取上下文信息"""
        context_indicators = ["背景", "情况", "场景", "环境"]
        for indicator in context_indicators:
            if indicator in prompt:
                start = prompt.find(indicator)
                end = prompt.find("。", start)
                if end != -1:
                    return prompt[start:end+1]
        return ""

    def _extract_requirements(self, prompt: str) -> List[str]:
        """提取具体要求"""
        requirements = []
        requirement_patterns = [
            r"要求：(.*?)(?:，|。|$)",
            r"需要(.*?)(?:，|。|$)",
            r"必须(.*?)(?:，|。|$)"
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, prompt)
            requirements.extend([match.strip() for match in matches])
        
        return requirements if requirements else ["生成高质量的回答"]

    def _extract_format(self, prompt: str) -> str:
        """提取输出格式"""
        for keyword, format_type in self.format_keywords.items():
            if keyword in prompt:
                return format_type
        return "paragraph"

    def _extract_tone(self, prompt: str) -> str:
        """提取语调风格"""
        for keyword, tone in self.tone_keywords.items():
            if keyword in prompt:
                return tone
        return "professional"

    def _classify_prompt_type(self, prompt: str) -> str:
        """分类提示词类型"""
        creative_keywords = ["创作", "想象", "创意", "故事"]
        analytical_keywords = ["分析", "评估", "比较", "研究"]
        instructional_keywords = ["教", "解释", "指导", "步骤"]
        
        if any(keyword in prompt for keyword in creative_keywords):
            return PromptType.CREATIVE.value
        elif any(keyword in prompt for keyword in analytical_keywords):
            return PromptType.ANALYTICAL.value
        elif any(keyword in prompt for keyword in instructional_keywords):
            return PromptType.INSTRUCTIONAL.value
        else:
            return PromptType.CONVERSATIONAL.value

    def optimize_prompt(self, natural_prompt: str) -> str:
        """优化提示词，返回JSON格式"""
        analysis = self.analyze_natural_prompt(natural_prompt)
        
        # 创建标准提示词结构
        optimized_prompt = PromptStructure(
            role=analysis["role"],
            task=analysis["task"],
            context=analysis["context"] or "用户需要专业的帮助",
            requirements=analysis["requirements"],
            format=analysis["format"],
            examples=self._generate_examples(analysis["prompt_type"]),
            constraints=self._generate_constraints(analysis["prompt_type"]),
            tone=analysis["tone"],
            prompt_type=analysis["prompt_type"]
        )
        
        # 转换为JSON格式
        return json.dumps(asdict(optimized_prompt), ensure_ascii=False, indent=2)

    def _generate_examples(self, prompt_type: str) -> List[str]:
        """根据类型生成示例"""
        examples_map = {
            "creative": ["示例：创作一个关于未来科技的短故事"],
            "analytical": ["示例：分析该策略的优缺点"],
            "instructional": ["示例：步骤1: 准备材料; 步骤2: 开始操作"],
            "conversational": ["示例：用户友好的对话方式回答"]
        }
        return examples_map.get(prompt_type, ["提供相关示例"])

    def _generate_constraints(self, prompt_type: str) -> List[str]:
        """根据类型生成约束条件"""
        constraints_map = {
            "creative": ["保持内容积极向上", "避免敏感话题"],
            "analytical": ["基于事实和数据", "保持客观性"],
            "instructional": ["步骤清晰明确", "易于理解和执行"],
            "conversational": ["语言自然流畅", "回答简洁明了"]
        }
        return constraints_map.get(prompt_type, ["遵循基本原则", "确保内容准确"])

def main():
    """主函数示例"""
    optimizer = PromptOptimizer()
    
    # 示例用法
    natural_prompt = "请帮我写一个关于人工智能发展的专业分析报告，要求详细分析现状和趋势"
    
    print("原始提示词：")
    print(natural_prompt)
    print("\n" + "="*50 + "\n")
    
    optimized_json = optimizer.optimize_prompt(natural_prompt)
    print("优化后的JSON提示词：")
    print(optimized_json)
    
    # 交互式使用
    print("\n" + "="*50 + "\n")
    print("交互式提示词优化器")
    while True:
        user_input = input("\n请输入您的自然语言提示词（输入'quit'退出）：")
        if user_input.lower() == 'quit':
            break
        
        try:
            result = optimizer.optimize_prompt(user_input)
            print("\n优化结果：")
            print(result)
        except Exception as e:
            print(f"处理错误：{e}")

if __name__ == "__main__":
    main()

