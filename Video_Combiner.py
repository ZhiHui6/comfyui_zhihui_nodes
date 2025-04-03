# 导入必要的库
import os  # 操作系统接口
import sys  # 系统相关参数和函数
import json  # JSON数据处理
import numpy as np  # 数值计算库
import datetime  # 日期时间处理
import torch  # PyTorch深度学习框架
from PIL import Image  # 图像处理库
import itertools  # 迭代工具
import folder_paths  # 自定义路径管理
from typing import List  # 类型提示
import cv2  # OpenCV视频处理库

class VideoCombine:
    """
    视频合并节点类，用于将图像序列合并为视频文件
    """
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点的输入参数类型
        返回:
            dict: 包含所有输入参数及其类型的字典
        """
        return {
            "required": {
                "images": ("IMAGE",),  # 输入图像序列
                "frame_rate": ("FLOAT", {"default": 8, "min": 1, "step": 1}),  # 帧率
                "filename_prefix": ("STRING", {"default": "AnimateDiff"}),  # 输出文件名前缀
                "format": (["video/mp4", "video/avi", "video/mkv", "video/mov", "video/wmv"], {}),  # 视频格式
                "pingpong": ("BOOLEAN", {"default": False}),  # 是否启用乒乓效果
                "save_output": ("BOOLEAN", {"default": True}),  # 是否保存输出
                "custom_output_path": ("STRING", {"default": ""})  # 自定义输出路径
            }
        }

    RETURN_TYPES = ("STRING",)  # 返回类型为字符串
    RETURN_NAMES = ("filename",)  # 返回名称为filename
    OUTPUT_NODE = True  # 标记为输出节点
    CATEGORY = "Video"  # 节点分类为视频
    FUNCTION = "combine_video"  # 主处理函数

    def combine_video(self, images, frame_rate, filename_prefix="AnimateDiff", 
                     format="video/mp4", pingpong=False, save_output=True, custom_output_path=""):
        """
        合并图像序列为视频文件
        
        参数:
            images: 输入图像序列，可以是torch.Tensor或numpy数组
            frame_rate: 输出视频的帧率
            filename_prefix: 输出文件名前缀
            format: 视频格式
            pingpong: 是否启用乒乓效果(来回播放)
            save_output: 是否保存输出文件
            custom_output_path: 自定义输出路径
        
        返回:
            tuple: 包含输出文件路径的元组
        """
        # 设置输出目录
        if custom_output_path and os.path.isdir(custom_output_path):
            output_dir = custom_output_path  # 使用自定义路径
        else:
            # 根据save_output标志选择输出或临时目录
            output_dir = folder_paths.get_output_directory() if save_output else folder_paths.get_temp_directory()

        os.makedirs(output_dir, exist_ok=True)  # 确保目录存在

        # 直接使用文件名，不添加计数器
        file = f"{filename_prefix}.mp4"
        file_path = os.path.join(output_dir, file)

        # 处理图像数据
        if isinstance(images, torch.Tensor):
            images = images.cpu().numpy()  # 将PyTorch张量转为numpy数组
        images = (images * 255).astype(np.uint8)  # 将0-1范围的浮点数转为0-255的整数
        
        # 处理 pingpong 效果
        if pingpong:
            # 将视频序列与反向序列(去掉首尾帧)拼接，实现来回播放效果
            images = np.concatenate([images, images[-2:0:-1]])

        # 获取视频尺寸
        height, width = images[0].shape[:2]
        
        # 根据格式选择对应的编码器和文件扩展名
        format_configs = {
            "video/mp4": ("mp4v", "mp4"),  # MP4格式配置
            "video/avi": ("XVID", "avi"),  # AVI格式配置
            "video/mkv": ("X264", "mkv"),  # MKV格式配置
            "video/mov": ("mp4v", "mov"),  # MOV格式配置
            "video/wmv": ("WMV2", "wmv")   # WMV格式配置
        }
        
        codec, ext = format_configs[format]  # 获取对应格式的编码器和扩展名
        file = f"{filename_prefix}.{ext}"  # 生成完整文件名
        file_path = os.path.join(output_dir, file)  # 生成完整文件路径

        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*codec)  # 创建视频编码器
        out = cv2.VideoWriter(file_path, fourcc, frame_rate, (width, height))  # 初始化视频写入器

        # 写入帧
        for img in images:
            # OpenCV 使用 BGR 格式，需要从RGB转换
            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            out.write(frame)  # 写入帧

        # 释放资源
        out.release()  # 关闭视频写入器

        return (file_path,)  # 返回文件路径

    def _get_next_counter(self, output_dir, filename_prefix):
        """
        获取下一个计数器值，用于生成唯一文件名
        
        参数:
            output_dir: 输出目录
            filename_prefix: 文件名前缀
        
        返回:
            int: 下一个可用的计数器值
        """
        max_counter = 0
        # 遍历目录中所有文件
        for f in os.listdir(output_dir):
            if f.startswith(filename_prefix):
                try:
                    # 从文件名中提取计数器值
                    counter = int(f.split("_")[-1].split(".")[0])
                    max_counter = max(max_counter, counter)  # 更新最大值
                except:
                    pass  # 忽略格式不匹配的文件
        return max_counter + 1  # 返回下一个计数器值

# 节点类映射，用于ComfyUI系统识别
NODE_CLASS_MAPPINGS = {
    "VideoCombine": VideoCombine
}

# 节点显示名称映射，用于UI界面显示
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoCombine": "🎬Video Combine"
}