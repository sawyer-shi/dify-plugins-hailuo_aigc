# author: sawyer-shi

import json
import logging
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)


class VideoDownloadTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """MiniMax video file download tool."""
        logger.info("Starting video download task (MiniMax)")

        try:
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                msg = "❌ API密钥未配置"
                logger.error(msg)
                yield self.create_text_message(msg)
                return

            file_id = tool_parameters.get("file_id")
            if file_id is None or str(file_id).strip() == "":
                msg = "❌ 请输入文件ID"
                logger.warning(msg)
                yield self.create_text_message(msg)
                return

            api_url = "https://api.minimaxi.com/v1/files/retrieve"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            params = {"file_id": int(file_id)}

            yield self.create_text_message("⬇️ 正在获取视频下载链接...")
            yield self.create_text_message(f"📁 文件ID: {file_id}")

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

            file_obj = resp_data.get("file")
            if not isinstance(file_obj, dict):
                yield self.create_text_message("❌ API 响应中未返回文件信息")
                return

            download_url = file_obj.get("download_url")
            filename = file_obj.get("filename") or f"{file_id}.mp4"

            if not download_url:
                yield self.create_text_message("❌ API 响应中未返回下载链接")
                return

            yield self.create_text_message(f"🔗 下载链接: {download_url}")
            yield self.create_text_message("⬇️ 正在下载视频文件...")

            try:
                video_response = requests.get(download_url, timeout=120)
            except requests.exceptions.RequestException as e:
                yield self.create_text_message(f"❌ 视频下载失败: {str(e)}")
                return

            if video_response.status_code != 200:
                yield self.create_text_message(
                    f"❌ 视频下载失败，状态码: {video_response.status_code}"
                )
                return

            yield self.create_blob_message(
                blob=video_response.content,
                meta={"mime_type": "video/mp4", "filename": filename},
            )
            yield self.create_text_message("✅ 视频下载完成")

            result_json = {
                "file": file_obj,
                "base_resp": resp_data.get("base_resp"),
            }
            yield self.create_json_message(result_json)

            logger.info("Video download completed")

        except Exception as e:
            error_msg = f"❌ 下载视频时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
