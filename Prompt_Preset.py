import comfy
import comfy.sd
import comfy.utils
import torch

class PromptPreset:
    """
    提示预设节点类，用于在ComfyUI中提供多个预设提示文本的选择功能
    
    功能：
    - 提供8个预设提示文本输入框，每个提示文本配有对应的标记注释
    - 允许用户通过下拉菜单选择其中一个预设作为输出
    - 输出选中的预设提示文本供后续节点使用
    
    使用场景：
    - 当需要快速切换不同风格的提示词时
    - 当需要管理多个常用提示词模板时
    - 当需要对比不同提示词生成效果时
    
    实现原理：
    - 通过INPUT_TYPES方法定义8组标记/提示文本输入框
    - 使用下拉选择框(Selected_Prompt)确定输出哪个预设
    - execute方法根据选择返回对应预设文本
    
    注意事项：
    - 预设编号从1开始计数
    - 如果选择的预设对应提示文本为空，将返回空字符串
    - 每个预设提示文本可以独立编辑，互不影响
    """
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入参数
        
        参数说明：
        - note_1到note_8: 8个标记输入框，用于简短描述对应提示文本的用途
          - 类型: STRING
          - 配置: 单行输入(multiline=False)
          - 默认值: 空字符串
          - 占位符: "标记1"到"标记8"
        - prompt_1到prompt_8: 8个多行文本输入框，用于输入预设提示文本
          - 类型: STRING
          - 配置: 多行输入(multiline=True)
          - 默认值: 空字符串
        - Selected_Prompt: 下拉选择框，用于选择要输出的预设编号(1-8)
          - 类型: 枚举列表["1","2","3","4","5","6","7","8"]
          - 配置: 默认值为空
        
        返回：
            dict: 包含8组标记/提示文本输入框和一个选择下拉框的配置
            
        数据结构示例:
        {
            "required": {
                "note_1": ("STRING", {"multiline": False, "default": "", "placeholder": "标记1"}),
                "prompt_1": ("STRING", {"multiline": True, "default": ""}),
                ...
                "Selected_Prompt": (["1",...,"8"], {"default": ""})
            }
        }
        """
        return {
            "required": {
                "note_1": ("STRING", {"multiline": False, "default": "", "placeholder": "标记1"}),
                "prompt_1": ("STRING", {"multiline": True, "default": ""}),
                "note_2": ("STRING", {"multiline": False, "default": "", "placeholder": "标记2"}),
                "prompt_2": ("STRING", {"multiline": True, "default": ""}),
                "note_3": ("STRING", {"multiline": False, "default": "", "placeholder": "标记3"}),
                "prompt_3": ("STRING", {"multiline": True, "default": ""}),
                "note_4": ("STRING", {"multiline": False, "default": "", "placeholder": "标记4"}),
                "prompt_4": ("STRING", {"multiline": True, "default": ""}),
                "note_5": ("STRING", {"multiline": False, "default": "", "placeholder": "标记5"}),
                "prompt_5": ("STRING", {"multiline": True, "default": ""}),
                "note_6": ("STRING", {"multiline": False, "default": "", "placeholder": "标记6"}),
                "prompt_6": ("STRING", {"multiline": True, "default": ""}),
                "note_7": ("STRING", {"multiline": False, "default": "", "placeholder": "标记7"}),
                "prompt_7": ("STRING", {"multiline": True, "default": ""}),
                "note_8": ("STRING", {"multiline": False, "default": "", "placeholder": "标记8"}),
                "prompt_8": ("STRING", {"multiline": True, "default": ""}),
                "note_9": ("STRING", {"multiline": False, "default": "", "placeholder": "标记9"}),
                "prompt_9": ("STRING", {"multiline": True, "default": ""}),
                "note_10": ("STRING", {"multiline": False, "default": "", "placeholder": "标记10"}),
                "prompt_10": ("STRING", {"multiline": True, "default": ""}),
                "Selected_Prompt": (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "execute"
    CATEGORY = "prompt"

    def execute(self, note_1, note_2, note_3, note_4, note_5, note_6, note_7, note_8, note_9, note_10, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6, prompt_7, prompt_8, prompt_9, prompt_10, Selected_Prompt):
        """
        执行节点逻辑，返回选中的预设提示文本
        
        参数：
            note_1到note_8 (str): 8个提示注释，用于标识对应提示文本的用途
              - 这些参数来自INPUT_TYPES中定义的标记输入框
              - 实际处理中未使用这些参数，仅用于保持参数一致性
            prompt_1到prompt_8 (str): 8个预设提示文本，包含完整的提示词内容
              - 这些参数来自INPUT_TYPES中定义的提示文本输入框
              - 内容可以是任意有效的提示词文本
            Selected_Prompt (str): 用户选择的预设编号(1-8)
              - 有效值为"1"到"8"的字符串
              - 用于确定输出哪个预设提示文本
            
        处理逻辑：
            1. 将所有提示文本存入列表prompts
              - 列表索引0对应预设1，索引7对应预设8
            2. 根据用户选择的预设编号获取对应提示文本
              - 将Selected_Prompt转换为整数并减1得到列表索引
            3. 返回包含选中提示文本的元组
              - 元组格式为("prompt",)以匹配RETURN_TYPES定义
            
        返回：
            tuple: 包含选中的提示文本的元组，格式为("prompt",)
              - 如果选择的预设对应文本为空，返回空字符串
              - 返回值会被后续节点作为输入使用
        
        注意事项：
            - 预设编号从1开始计数，但列表索引从0开始
            - 如果选择的预设编号对应提示文本为空，将返回空字符串
            - 所有预设提示文本可以独立编辑，互不影响
            - 该方法不修改任何预设内容，仅做选择输出
        """
        prompts = [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5,
                  prompt_6, prompt_7, prompt_8, prompt_9, prompt_10]
        return (prompts[int(Selected_Prompt)-1],)

# 节点类映射，将节点类注册到ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptPreset": PromptPreset
}

# 节点显示名称映射，定义节点在UI中的显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptPreset": "💬Prompt Preset"
}