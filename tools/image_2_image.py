# author: sawyer-shi

import base64
import json
import logging
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .image_utils import encode_image_input

logger = logging.getLogger(__name__)


class Image2ImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """MiniMax image-to-image tool."""
        logger.info("Starting image-to-image task (MiniMax)")

        try:
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                msg = "❌ API密钥未配置"
                logger.error(msg)
                yield self.create_text_message(msg)
                return

            prompt = tool_parameters.get("prompt", "").strip()
            if not prompt:
                msg = "❌ 请输入提示词"
                logger.warning(msg)
                yield self.create_text_message(msg)
                return

            subject_image = tool_parameters.get("subject_image")
            if not subject_image:
                msg = "❌ 请提供主体参考图片"
                logger.warning(msg)
                yield self.create_text_message(msg)
                return

            model = tool_parameters.get("model", "image-01")
            aspect_ratio = tool_parameters.get("aspect_ratio", "1:1")
            response_format = tool_parameters.get("response_format", "url")
            n = int(tool_parameters.get("n", 1))
            prompt_optimizer = tool_parameters.get("prompt_optimizer", "false") == "true"
            aigc_watermark = tool_parameters.get("aigc_watermark", "false") == "true"
            width = tool_parameters.get("width")
            height = tool_parameters.get("height")
            seed = tool_parameters.get("seed")

            if n < 1:
                n = 1
            if n > 9:
                n = 9

            try:
                image_file = encode_image_input(subject_image, max_bytes=10 * 1024 * 1024)
            except Exception as e:
                yield self.create_text_message(f"❌ 图像处理失败: {str(e)}")
                return

            payload: dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "subject_reference": [
                    {
                        "type": "character",
                        "image_file": image_file,
                    }
                ],
                "aspect_ratio": aspect_ratio,
                "response_format": response_format,
                "n": n,
                "prompt_optimizer": prompt_optimizer,
                "aigc_watermark": aigc_watermark,
            }
            if seed is not None and seed != "":
                payload["seed"] = int(seed)
            if width and height:
                payload["width"] = int(width)
                payload["height"] = int(height)

            api_url = "https://api.minimaxi.com/v1/image_generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            yield self.create_text_message("🚀 图生图任务启动中...")
            yield self.create_text_message(f"🤖 使用模型: {model}")
            yield self.create_text_message(
                f"📝 提示词: {prompt[:50]}{'...' if len(prompt) > 50 else ''}"
            )
            yield self.create_text_message("⏳ 正在连接 MiniMax API...")

            logger.info("Submitting request: %s", json.dumps(payload, ensure_ascii=False))
            yield self.create_text_message("🎨 正在生成图像，请稍候...")

            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=120,
                )
            except requests.exceptions.Timeout:
                msg = "❌ 请求超时，请稍后重试"
                logger.error(msg)
                yield self.create_text_message(msg)
                return
            except requests.exceptions.RequestException as e:
                msg = f"❌ 请求失败: {str(e)}"
                logger.error(msg)
                yield self.create_text_message(msg)
                return

            if response.status_code != 200:
                logger.error(
                    "API status %s: %s", response.status_code, response.text[:300]
                )
                yield self.create_text_message(
                    f"❌ API 响应状态码: {response.status_code}"
                )
                if response.text:
                    yield self.create_text_message(
                        f"🔧 响应内容: {response.text[:500]}"
                    )
                return

            try:
                resp_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(
                    "Failed to parse JSON: %s - %s", str(e), response.text[:300]
                )
                yield self.create_text_message("❌ API 响应解析失败（非JSON）")
                return

            data = resp_data.get("data", {})
            if not isinstance(data, dict):
                yield self.create_text_message("❌ API 响应中未返回图像数据")
                return

            if response_format == "base64":
                images = data.get("image_base64", [])
            else:
                images = data.get("image_urls", [])

            if not images:
                yield self.create_text_message("❌ API 响应中未返回图像内容")
                return

            yield self.create_text_message("🎉 图像生成成功！")

            if response_format == "base64":
                for i, image_item in enumerate(images):
                    if not isinstance(image_item, str):
                        yield self.create_text_message(
                            f"❌ 第 {i + 1} 张图片 Base64 数据无效"
                        )
                        return
                    try:
                        image_bytes = base64.b64decode(image_item)
                    except Exception as e:
                        yield self.create_text_message(
                            f"❌ 处理第 {i + 1} 张图片失败: {str(e)}"
                        )
                        return
                    yield self.create_blob_message(
                        blob=image_bytes,
                        meta={"mime_type": "image/png"},
                    )
                    yield self.create_text_message(f"✅ 第 {i + 1} 张图片生成完成！")
            else:
                for i, image_item in enumerate(images):
                    image_url = str(image_item)
                    yield self.create_image_message(image_url)
                    yield self.create_text_message(f"✅ 第 {i + 1} 张图片生成完成！")

            metadata = resp_data.get("metadata")
            if metadata:
                yield self.create_text_message("📊 生成统计:")
                for key, value in metadata.items():
                    yield self.create_text_message(f"  - {key}: {value}")

            yield self.create_text_message("🎯 图生图任务完成！")
            logger.info("Image-to-image task completed")

        except Exception as e:
            error_msg = f"❌ 生成图像时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
