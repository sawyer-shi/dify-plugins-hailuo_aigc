# 海螺 AIGC

一个强大的 Dify 插件，使用 MiniMax 海螺模型提供全面的 AI 图像和视频生成功能。支持文生图、图生图（主体参考）、文生视频、图生视频、首尾帧视频、主体参考视频、视频结果查询（可选下载）等多种生成模式，具有专业级质量和灵活的配置选项。

## 版本信息

- **当前版本**: v0.0.1
- **发布日期**: 2026-02-22
- **兼容性**: Dify 插件框架
- **Python 版本**: 3.12

### 版本历史
- **v0.0.1** (2026-02-22): 初始版本，包含图像和视频生成功能

## 快速开始

1. 在您的 Dify 环境中安装插件
2. 配置 MiniMax API 凭证（API Key）
3. 开始使用 AI 生成图像和视频

## 核心特性
<img width="368" height="639" alt="CN" src="https://github.com/user-attachments/assets/d7b4e80e-8760-458f-8e0f-15c7ba685e19" /><img width="366" height="717" alt="EN" src="https://github.com/user-attachments/assets/de184d01-d02f-4904-87b2-800135628ad3" />

- **多种生成模式**: 文生图、图生图、文生视频、图生视频、首尾帧视频、主体参考视频
- **最新 AI 模型**: 支持 MiniMax-Hailuo-2.3、MiniMax-Hailuo-2.3-Fast、MiniMax-Hailuo-02、T2V-01-Director、I2V-01-Director、I2V-01-live、I2V-01、S2V-01、image-01、image-01-live
- **灵活的图像尺寸**: 多种宽高比，从 1:1 到 21:9
- **视频生成**: 任务异步生成，支持状态查询与下载
- **首尾帧视频**: 从首帧和尾帧图像生成视频
- **主体参考视频**: 基于主体参考图生成视频
- **水印控制**: 可选 AIGC 水印

## 核心功能

### 图像生成

#### 文生图 (text_2_image)
使用 MiniMax 图像模型根据文本描述生成图像。
- **支持模型**: image-01, image-01-live
- **功能特性**:
  - 多种宽高比（1:1、4:3、3:4、16:9、9:16、3:2、2:3、21:9）
  - 可选水印
  - 可选提示词优化
  - image-01-live 支持画风参数

#### 图生图 (image_2_image)
根据文本和主体参考图像生成图像。
- **支持模型**: image-01, image-01-live
- **功能特性**:
  - 主体参考（人物）
  - 多种宽高比
  - 可选水印
  - 参考图像支持 jpeg/png/webp，最大 10MB

### 视频生成

#### 文生视频 (text_2_video)
根据文本创建视频生成任务。
- **支持模型**: MiniMax-Hailuo-2.3, MiniMax-Hailuo-02, T2V-01-Director, T2V-01
- **功能特性**:
  - 任务异步生成
  - 分辨率：720P、768P、1080P
  - 可选提示词优化与快速预处理

#### 图生视频 (image_2_video)
根据单张图片创建视频生成任务。
- **支持模型**: MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast, MiniMax-Hailuo-02, I2V-01-Director, I2V-01-live, I2V-01
- **功能特性**:
  - 单张图片作为首帧
  - 分辨率：512P、720P、768P、1080P
  - 可选提示词优化与快速预处理

#### 首尾帧视频 (images_2_video)
根据首帧和尾帧图像创建视频生成任务。
- **支持模型**: MiniMax-Hailuo-02
- **功能特性**:
  - 首帧 + 尾帧输入
  - 分辨率：768P、1080P

#### 主体参考视频 (subject_reference_2_video)
根据主体参考图创建视频生成任务。
- **支持模型**: S2V-01
- **功能特性**:
  - 主体参考（人物）
  - 单张参考图输入

#### 视频结果查询 (video_query)
查询视频生成任务状态并可选下载视频。
- **功能特性**:
  - 实时任务状态
  - 下载链接获取
  - 状态成功时可直接下载

## 系统要求

- Python 3.12
- Dify 平台访问权限
- MiniMax API 凭证（API Key）
- 所需的 Python 包（通过 requirements.txt 安装）:
  - dify_plugin>=0.2.0
  - requests>=2.31.0,<3.0.0
  - pillow>=10.0.0,<11.0.0

## 安装与配置

1. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 在插件设置中配置 MiniMax API 凭证：
   - **API Key**: 您的 MiniMax API 密钥
   - 获取地址：https://platform.minimaxi.com/user-center/basic-information/interface-key

3. 在您的 Dify 环境中安装插件

## 使用方法

### 图像生成工具

#### 1. 文生图
- **参数**:
  - `prompt`: 图像文本描述（必需）
  - `model`: image-01 / image-01-live
  - `aspect_ratio`: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
  - `response_format`: url / base64
  - `n`: 1-9
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false
  - `style_type` / `style_weight`（仅 image-01-live）

#### 2. 图生图
- **参数**:
  - `prompt`: 文本描述（必需）
  - `subject_image`: 主体参考图（必需）
  - `model`: image-01 / image-01-live
  - `aspect_ratio`: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
  - `response_format`: url / base64
  - `n`: 1-9
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

### 视频生成工具

#### 3. 文生视频
- **参数**:
  - `prompt`: 文本描述（必需）
  - `model`: MiniMax-Hailuo-2.3 / MiniMax-Hailuo-02 / T2V-01-Director / T2V-01
  - `resolution`: 720P / 768P / 1080P
  - `duration`: 6 或 10（取决于模型与分辨率）
  - `prompt_optimizer`: true / false
  - `fast_pretreatment`: true / false（仅 Hailuo 2.3/02）
  - `aigc_watermark`: true / false

#### 4. 图生视频
- **参数**:
  - `first_frame_image`: 首帧图片（必需）
  - `prompt`: 可选文本描述
  - `model`: MiniMax-Hailuo-2.3 / MiniMax-Hailuo-2.3-Fast / MiniMax-Hailuo-02 / I2V-01-Director / I2V-01-live / I2V-01
  - `resolution`: 512P / 720P / 768P / 1080P
  - `duration`: 6 或 10（取决于模型与分辨率）
  - `prompt_optimizer`: true / false
  - `fast_pretreatment`: true / false（仅 Hailuo 2.3/02）
  - `aigc_watermark`: true / false

#### 5. 首尾帧视频
- **参数**:
  - `first_frame_image`: 首帧图片（必需）
  - `last_frame_image`: 尾帧图片（必需）
  - `prompt`: 可选文本描述
  - `model`: MiniMax-Hailuo-02
  - `resolution`: 768P / 1080P
  - `duration`: 6 或 10（取决于分辨率）
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

#### 6. 主体参考视频
- **参数**:
  - `subject_image`: 主体参考图（必需）
  - `prompt`: 可选文本描述
  - `model`: S2V-01
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

#### 7. 视频结果查询
- **参数**:
  - `task_id`: 视频生成任务 ID（必需）
  - `download_video`: 当视频可用时下载视频文件（默认：启用）

## 注意事项

- 视频生成是异步的，使用视频结果查询工具检查状态并获取结果
- 首尾帧视频仅支持 MiniMax-Hailuo-02
- 主体参考视频当前仅支持单主体参考图
- 参考图像大小建议：图像 <= 10MB，视频 <= 20MB

## 开发者信息

- **作者**: `https://github.com/sawyer-shi`
- **邮箱**: sawyer36@foxmail.com
- **许可证**: Apache License 2.0
- **源代码**: `https://github.com/sawyer-shi/dify-plugins-hailuo_aigc`
- **支持**: 通过 Dify 平台和 GitHub Issues 提供

## 许可证声明

本项目采用 Apache License 2.0 许可证。完整的许可证文本请参阅 [LICENSE](LICENSE) 文件。

---

**准备好使用 AI 创建精美的图像和视频了吗？**
