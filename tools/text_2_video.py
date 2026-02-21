# author: sawyer-shi

import json
import logging
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)


class Text2VideoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """MiniMax text-to-video tool."""
        logger.info("Starting text-to-video task (MiniMax)")

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

            model = tool_parameters.get("model", "MiniMax-Hailuo-2.3")
            duration = tool_parameters.get("duration", 6)
            resolution = tool_parameters.get("resolution", "768P")
            prompt_optimizer = tool_parameters.get("prompt_optimizer", "true") == "true"
            fast_pretreatment = tool_parameters.get("fast_pretreatment", "false") == "true"
            callback_url = tool_parameters.get("callback_url")
            aigc_watermark = tool_parameters.get("aigc_watermark", "false") == "true"

            payload: dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "prompt_optimizer": prompt_optimizer,
                "aigc_watermark": aigc_watermark,
            }
            if duration is not None and str(duration).strip() != "":
                payload["duration"] = int(duration)
            if resolution:
                payload["resolution"] = resolution
            if fast_pretreatment and model in ("MiniMax-Hailuo-2.3", "MiniMax-Hailuo-02"):
                payload["fast_pretreatment"] = fast_pretreatment
            if callback_url:
                payload["callback_url"] = callback_url

            api_url = "https://api.minimaxi.com/v1/video_generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            yield self.create_text_message("🚀 文生视频任务启动中...")
            yield self.create_text_message(f"🤖 使用模型: {model}")
            yield self.create_text_message(
                f"📝 提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}"
            )
            yield self.create_text_message("⏳ 正在连接 MiniMax API...")

            logger.info("Submitting request: %s", json.dumps(payload, ensure_ascii=False))
            yield self.create_text_message("🎬 正在提交视频生成任务...")

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

            task_id = resp_data.get("task_id")
            if not task_id:
                yield self.create_text_message("❌ API 响应中未返回任务ID")
                return

            yield self.create_text_message(f"📋 视频生成任务已提交，任务ID: {task_id}")
            yield self.create_text_message("✅ 任务提交成功，可用任务ID查询状态")
            yield self.create_text_message("🎯 文生视频任务提交完成！")

            result_json = {
                "task_id": task_id,
                "status": "submitted",
                "message": "文生视频任务已提交",
            }
            yield self.create_json_message(result_json)

            logger.info("Text-to-video task submitted")

        except Exception as e:
            error_msg = f"❌ 生成视频时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
