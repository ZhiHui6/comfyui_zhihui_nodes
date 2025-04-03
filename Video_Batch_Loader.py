import os
import torch
import numpy as np
import cv2
import folder_paths

# 定义最大数值常量
BIGMAX = 9999999  # 视频索引最大值
DIMMAX = 8192     # 视频宽高最大值

class VideoSequenceProcessor:
    """
    视频序列处理类，用于批量加载和处理视频文件
    """
    # 添加持久化的类变量
    _current_index = 0      # 当前视频索引
    _last_directory = None  # 上次处理的目录路径
    _video_files = []       # 视频文件列表缓存

    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点的输入参数类型
        """
        return {
            "required": {
                "directory": ("STRING", {
                    "placeholder": "Video folder path",
                    "default": folder_paths.get_input_directory(),  # 默认输入目录
                }),
                "mode": (["Single video", "Next video", "Random video"], {"default": "Single video"}),
                "video_index": ("INT", {"default": 0, "min": 0, "max": BIGMAX, "step": 1}),
                "frames_per_video": ("INT", {"default": 8, "min": 1, "max": BIGMAX, "step": 1}),
                "custom_width": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
                "custom_height": ("INT", {"default": 0, "min": 0, "max": DIMMAX, "step": 8}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "STRING")
    RETURN_NAMES = ("frames", "current_index", "total_videos", "filename_text")
    FUNCTION = "process_sequence"
    CATEGORY = "Loader/Video"

    @classmethod
    def process_sequence(cls, directory, mode="单个视频", video_index=0, frames_per_video=8, custom_width=0, custom_height=0):
        """
        处理视频序列的主方法
        
        参数:
            directory: 视频目录路径
            mode: 视频选择模式(单个视频/下一个视频/随机视频)
            video_index: 视频索引(仅用于单个视频模式)
            frames_per_video: 每视频提取帧数
            custom_width: 自定义输出宽度(0表示保持原尺寸)
            custom_height: 自定义输出高度(0表示保持原尺寸)
        """
        # 检查目录是否存在
        if not os.path.isdir(directory):
            raise ValueError(f"Directory does not exist: {directory}")

        # 检查目录是否改变
        if cls._last_directory != directory:
            cls._current_index = 0  # 重置索引
            cls._last_directory = directory  # 更新目录缓存
            # 重新扫描视频文件
            cls._video_files = []
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']  # 支持的视频格式
            for file in os.listdir(directory):
                # 检查文件扩展名是否匹配
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    cls._video_files.append(os.path.join(directory, file))  # 添加完整路径

        if not cls._video_files:
            raise ValueError(f"No video files found in directory: {directory}")

        # 根据模式选择视频
        if mode == "单个视频":
            selected_index = min(video_index, len(cls._video_files) - 1)  # 确保不越界
        elif mode == "下一个视频":
            selected_index = cls._current_index
            cls._current_index = (cls._current_index + 1) % len(cls._video_files)  # 循环索引
        else:  # 随机视频
            selected_index = np.random.randint(0, len(cls._video_files))  # 随机选择

        video_path = cls._video_files[selected_index]
        filename = os.path.basename(video_path)  # 获取文件名
        
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")  # 视频打开失败错误

        frames = []  # 存储提取的帧
        frame_count = 0
        # 读取指定数量的帧
        while frame_count < frames_per_video:
            ret, frame = cap.read()  # 读取一帧
            if not ret:  # 读取失败或视频结束
                break

            if custom_width > 0 and custom_height > 0:
                frame = cv2.resize(frame, (custom_width, custom_height))
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
            frame_count += 1

        cap.release()

        if not frames:
            raise ValueError("Failed to read video frames")

        frames_tensor = torch.from_numpy(np.stack(frames))
        return (frames_tensor, selected_index, len(cls._video_files), filename)

    @classmethod
    def IS_CHANGED(cls, directory, mode, **kwargs):
        """
        判断节点是否需要更新
        """
        if mode == "下一个视频":
            # 对于"下一个视频"模式，每次都返回不同的值以触发更新
            return float("nan")
        if not directory or not isinstance(directory, str):
            directory = folder_paths.get_input_directory()
        if not os.path.isdir(directory):
            return ""
        return os.path.getmtime(directory)

    @classmethod
    def VALIDATE_INPUTS(cls, directory, **kwargs):
        """
        验证输入参数的有效性
        """
        if not directory or not isinstance(directory, str):
            directory = folder_paths.get_input_directory()  # 使用默认目录
        if not os.path.isdir(directory):
            return "Invalid directory path: {}".format(directory)  # 返回错误信息
        return True  # 输入有效

# 注册节点到ComfyUI系统
NODE_CLASS_MAPPINGS = {
    "VideoSequenceProcessor": VideoSequenceProcessor  # 节点名称与类映射
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoSequenceProcessor": "🎬Video Batch Loader"  # 节点显示名称
}