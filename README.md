# Hailuo AIGC

A powerful Dify plugin providing comprehensive AI-powered image and video generation capabilities using MiniMax Hailuo models. Supports text-to-image, image-to-image with subject reference, text-to-video, image-to-video, first-last frame video, subject reference video, and video result query with optional download.

## Version Information

- **Current Version**: v0.0.1
- **Release Date**: 2026-02-22
- **Compatibility**: Dify Plugin Framework
- **Python Version**: 3.12

### Version History
- **v0.0.1** (2026-02-22): Initial release with image and video generation capabilities

## Quick Start

1. Install the plugin in your Dify environment
2. Configure your MiniMax API credentials (API Key)
3. Start generating images and videos with AI

## Key Features
<img width="368" height="639" alt="CN" src="https://github.com/user-attachments/assets/d7b4e80e-8760-458f-8e0f-15c7ba685e19" /><img width="366" height="717" alt="EN" src="https://github.com/user-attachments/assets/de184d01-d02f-4904-87b2-800135628ad3" />

- **Multiple Generation Modes**: Text-to-image, image-to-image, text-to-video, image-to-video, first-last frame video, subject reference video
- **Latest AI Models**: Supports MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast, MiniMax-Hailuo-02, T2V-01-Director, I2V-01-Director, I2V-01-live, I2V-01, S2V-01, image-01, image-01-live
- **Flexible Image Ratios**: Multiple aspect ratios from 1:1 to 21:9
- **Video Generation**: Task-based asynchronous generation with status query and download
- **First-Last Frame Video**: Create videos from first and last frame images
- **Subject Reference Video**: Create videos using subject reference images
- **Watermark Control**: Optional AIGC watermark for content authenticity

## Core Features

### Image Generation

#### Text to Image (text_2_image)
Generate images from text descriptions using MiniMax image models.
- **Supported Models**: image-01, image-01-live
- **Features**:
  - Multiple aspect ratios (1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9)
  - Optional watermark
  - Optional prompt optimizer
  - Style options for image-01-live

#### Image to Image (image_2_image)
Generate images from text and a subject reference image.
- **Supported Models**: image-01, image-01-live
- **Features**:
  - Subject reference guidance (character)
  - Multiple aspect ratios
  - Optional watermark
  - Reference image (jpeg/png/webp; max 10MB)

### Video Generation

#### Text to Video (text_2_video)
Create a video generation task from text.
- **Supported Models**: MiniMax-Hailuo-2.3, MiniMax-Hailuo-02, T2V-01-Director, T2V-01
- **Features**:
  - Task-based async generation
  - Resolution: 720P, 768P, 1080P
  - Optional prompt optimizer and fast pretreatment

#### Image to Video (image_2_video)
Create a video generation task from a single image.
- **Supported Models**: MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast, MiniMax-Hailuo-02, I2V-01-Director, I2V-01-live, I2V-01
- **Features**:
  - Single image input as first frame
  - Resolution: 512P, 720P, 768P, 1080P
  - Optional prompt optimizer and fast pretreatment

#### First-Last Frame Video (images_2_video)
Create a video generation task from first and last frame images.
- **Supported Models**: MiniMax-Hailuo-02
- **Features**:
  - First and last frame inputs
  - Resolution: 768P, 1080P

#### Subject Reference Video (subject_reference_2_video)
Create a video generation task using a subject reference image.
- **Supported Models**: S2V-01
- **Features**:
  - Subject reference guidance (character)
  - Single reference image input

#### Video Result Query (video_query)
Query video generation task status and optionally download the video.
- **Features**:
  - Real-time task status
  - Download URL retrieval
  - Optional file download when status is Success

## Requirements

- Python 3.12
- Dify Platform access
- MiniMax API credentials (API Key)
- Required Python packages (installed via requirements.txt):
  - dify_plugin>=0.2.0
  - requests>=2.31.0,<3.0.0
  - pillow>=10.0.0,<11.0.0

## Installation & Configuration

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your MiniMax API credentials in the plugin settings:
   - **API Key**: Your MiniMax API key
   - Get API key: https://platform.minimaxi.com/user-center/basic-information/interface-key

3. Install the plugin in your Dify environment

## Usage

### Image Generation Tools

#### 1. Text to Image
- **Parameters**:
  - `prompt`: Text description of the image (required)
  - `model`: image-01 / image-01-live
  - `aspect_ratio`: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
  - `response_format`: url / base64
  - `n`: 1-9
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false
  - `style_type` / `style_weight` (image-01-live only)

#### 2. Image to Image
- **Parameters**:
  - `prompt`: Text description (required)
  - `subject_image`: Subject reference image (required)
  - `model`: image-01 / image-01-live
  - `aspect_ratio`: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
  - `response_format`: url / base64
  - `n`: 1-9
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

### Video Generation Tools

#### 3. Text to Video
- **Parameters**:
  - `prompt`: Text description (required)
  - `model`: MiniMax-Hailuo-2.3 / MiniMax-Hailuo-02 / T2V-01-Director / T2V-01
  - `resolution`: 720P / 768P / 1080P
  - `duration`: 6 or 10 (depends on model/resolution)
  - `prompt_optimizer`: true / false
  - `fast_pretreatment`: true / false (Hailuo 2.3/02 only)
  - `aigc_watermark`: true / false

#### 4. Image to Video
- **Parameters**:
  - `first_frame_image`: Input image (required)
  - `prompt`: Optional text description
  - `model`: MiniMax-Hailuo-2.3 / MiniMax-Hailuo-2.3-Fast / MiniMax-Hailuo-02 / I2V-01-Director / I2V-01-live / I2V-01
  - `resolution`: 512P / 720P / 768P / 1080P
  - `duration`: 6 or 10 (depends on model/resolution)
  - `prompt_optimizer`: true / false
  - `fast_pretreatment`: true / false (Hailuo 2.3/02 only)
  - `aigc_watermark`: true / false

#### 5. First-Last Frame Video
- **Parameters**:
  - `first_frame_image`: First frame image (required)
  - `last_frame_image`: Last frame image (required)
  - `prompt`: Optional text description
  - `model`: MiniMax-Hailuo-02
  - `resolution`: 768P / 1080P
  - `duration`: 6 or 10 (depends on resolution)
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

#### 6. Subject Reference Video
- **Parameters**:
  - `subject_image`: Subject reference image (required)
  - `prompt`: Optional text description
  - `model`: S2V-01
  - `prompt_optimizer`: true / false
  - `aigc_watermark`: true / false

#### 7. Video Result Query
- **Parameters**:
  - `task_id`: Video generation task ID (required)
  - `download_video`: Download video file when available (default: true)

## Notes

- Video generation is asynchronous; use Video Result Query to check status and retrieve results
- First/last frame video uses MiniMax-Hailuo-02 only
- Subject reference video currently supports a single subject image
- Reference images should be under 10MB (image) or 20MB (video) in size

## Developer Information

- **Author**: `https://github.com/sawyer-shi`
- **Email**: sawyer36@foxmail.com
- **License**: Apache License 2.0
- **Source Code**: `https://github.com/sawyer-shi/dify-plugins-hailuo_aigc`
- **Support**: Through Dify platform and GitHub Issues

## License Notice

This project is licensed under Apache License 2.0. See [LICENSE](LICENSE) file for full license text.

---

**Ready to create stunning images and videos with AI?**
