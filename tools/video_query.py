# author: sawyer-shi

import json
import logging
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)


class VideoQueryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """MiniMax video generation status query tool."""
        logger.info("Starting video query task (MiniMax)")

        try:
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                msg = "❌ API密钥未配置"
                logger.error(msg)
                yield self.create_text_message(msg)
                return

            task_id = tool_parameters.get("task_id", "").strip()
            if not task_id:
                msg = "❌ 请输入任务ID"
                logger.warning(msg)
                yield self.create_text_message(msg)
                return

            api_url = "https://api.minimaxi.com/v1/query/video_generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            params = {"task_id": task_id}

            yield self.create_text_message("🔍 正在查询视频生成结果...")
            yield self.create_text_message(f"📋 任务ID: {task_id}")
            yield self.create_text_message("⏳ 正在连接 MiniMax API...")

            try:
                response = requests.get(api_url, headers=headers, params=params, timeout=60)
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

            status = resp_data.get("status")
            file_id = resp_data.get("file_id")
            video_width = resp_data.get("video_width")
            video_height = resp_data.get("video_height")

            yield self.create_text_message("✅ 查询成功")
            yield self.create_text_message(f"📊 状态: {status}")
            if file_id:
                yield self.create_text_message(f"📁 文件ID: {file_id}")
            if video_width and video_height:
                yield self.create_text_message(
                    f"📐 分辨率: {video_width}x{video_height}"
                )

            result_json = {
                "task_id": resp_data.get("task_id"),
                "status": status,
                "file_id": file_id,
                "video_width": video_width,
                "video_height": video_height,
                "base_resp": resp_data.get("base_resp"),
            }
            yield self.create_json_message(result_json)

            logger.info("Video query completed")

        except Exception as e:
            error_msg = f"❌ 查询视频结果时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
