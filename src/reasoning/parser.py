# 此文件用于定义与 LLM 的交互接口

class ConstraintParser:
    def __init__(self, model_name="Qwen/Qwen2.5-7B-Instruct"):
        self.model_name = model_name
        # 在魔搭环境加载模型...
        
    def parse_query(self, user_text):
        """
        输入用户像'沙发挡路吗'这样的文本
        输出 JSON 格式的几何检查任务
        """
        pass

class AdviceGenerator:
    def __init__(self):
        pass
        
    def generate(self, violation_json):
        """
        根据几何层返回的违规数据生成的建议
        """
        pass
