[English](README.md) | [简体中文](README_CN.md)  

# ComfyUI_ZhiHui_Node
This is a custom node package for [ComfyUI], currently containing three nodes.

## Node Introduction
### 1. Prompt Preset
- **Function**: Provides selection of 10 preset prompt texts
- **Key Features**:
  - Each preset comes with marker comments and prompt text input box
  - Output preset selection via dropdown menu
  - Supports multi-line text input
- **Use Cases**:
  - Quickly switch between different style prompts
  - Manage commonly used prompt templates
  - Compare generation effects of different prompts
- **Notes**:
  - Preset numbering starts from 1
  - Empty prompt text will return empty string
  - All presets can be edited independently

### 2. Video Batch Loader
- **Function**: Batch load video frames from directory
- **Modes**: 
  - Load by index
  - Auto sequential loading
  - Random selection
- **Parameters**:
  - Frame size adjustment
  - Frame count limit
  - Frame rate override
- **Use Cases**:
  - Dataset preparation
  - Animation workflow
  - Video analysis preprocessing

### 3. Video Combiner
- **Function**: Combine image sequences into video files
- **Supported Formats**: MP4, AVI, MKV, MOV, WMV
- **Advanced Features**:
  - Ping-pong loop effect
  - Custom frame rate (1-60fps)
  - Custom output path
  - Auto filename generation
- **Input Requirements**:
  - Image sequences must be in RGB format
  - Supports PyTorch tensors or numpy arrays
- **Output Control**:
  - Option to save to output directory or temp directory
  - Supports overwrite or append mode

## Installation
### Via ComfyUI Manager (Recommended)
1. Install the ComfyUI Manager Manager
2. In Manager, "Install via Git URL"
3. Enter https://github.com/ZhiHui6/comfyui_zhihui_nodes.git
4. Click Install
5. Restart ComfyUI
6. In the Nodes tab of ComfyUI, you should be able to see the newly added nodes.

### Manual Installation
1. Download the entire node folder
2. Copy the entire custom node folder ComfyUI_ZhiHui_Node to ComfyUI's custom_nodes directory
3. Restart ComfyUI
4. You should see the new nodes in ComfyUI's node tab.

## Contact
- **Rednote**: https://www.xiaohongshu.com/user/profile/5a7cf88d11be105c8d32d9c7
- **LibLib Art**: https://www.liblib.art/userpage/5014246d17704c4f821537a3abfd9c3d
