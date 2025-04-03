[English](README.md) | [简体中文](README_CN.md)  

# ComfyUI_ZhiHui_Node
这是一个针对[ComfyUI]的自定义节点包,目前包含三个节点。

## 节点介绍
### 1. Prompt Preset
- **功能**: 提供10个预设提示文本的选择功能
- **核心特性**:
  - 每个预设配有标记注释和提示文本输入框
  - 通过下拉菜单选择输出预设
  - 支持多行文本输入
- **应用场景**:
  - 快速切换不同风格提示词
  - 管理常用提示词模板
  - 对比不同提示词生成效果
- **注意事项**:
  - 预设编号从1开始
  - 空提示文本将返回空字符串
  - 所有预设可独立编辑

### 2. Video Batch Loader
- **功能**: 从目录批量加载视频帧
- **工作模式**: 
  - 按索引加载
  - 自动顺序加载
  - 随机选择
- **参数设置**:
  - 帧尺寸调整
  - 帧数限制
  - 帧率覆盖
- **应用场景**:
  - 数据集准备
  - 动画工作流程
  - 视频分析预处理

### 3. Video Combiner
- **功能**: 将图像序列合并为视频文件
- **支持格式**: MP4、AVI、MKV、MOV、WMV
- **高级功能**:
  - 乒乓循环效果
  - 自定义帧率(1-60fps)
  - 自定义输出路径
  - 自动文件名生成
- **输入要求**:
  - 图像序列需为RGB格式
  - 支持PyTorch张量或numpy数组
- **输出控制**:
  - 可选择保存到输出目录或临时目录
  - 支持覆盖或追加模式

## 安装方式
### 通过 ComfyUI Manager 安装（推荐）
1. 安装ComfyUI管理器 Manager
2. 在 Manager 中搜索 ComfyUI_ZhiHui_Node
3. 点击 Install 安装
4. 重启ComfyUI
5. 在ComfyUI的节点选项卡中，你应该可以看到新添加的节点。

### 手动安装
1. 下载整个节点文件夹
2. 将整个自定义节点文件夹 ComfyUI_ZhiHui_Node 复制到ComfyUI的 custom_nodes 目录下
3. 重启ComfyUI
4. 在ComfyUI的节点选项卡中，你应该可以看到新添加的节点。

## 社交联络
- **小红书**：https://www.xiaohongshu.com/user/profile/5a7cf88d11be105c8d32d9c7
- **哩布哩布**：https://www.liblib.art/userpage/5014246d17704c4f821537a3abfd9c3d
