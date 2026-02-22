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

            download_video = tool_parameters.get("download_video", "true") == "true"

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

            download_url = None
            if status == "Success" and file_id:
                file_api_url = "https://api.minimaxi.com/v1/files/retrieve"
                file_params = {"file_id": int(file_id)}
                try:
                    file_response = requests.get(
                        file_api_url, headers=headers, params=file_params, timeout=60
                    )
                except requests.exceptions.RequestException as e:
                    yield self.create_text_message(f"❌ 获取下载链接失败: {str(e)}")
                    file_response = None

                if file_response and file_response.status_code == 200:
                    try:
                        file_data = file_response.json()
                    except json.JSONDecodeError:
                        file_data = None
                    if isinstance(file_data, dict):
                        file_obj = file_data.get("file", {})
                        download_url = file_obj.get("download_url")
                        filename = file_obj.get("filename") or f"{file_id}.mp4"

                        if download_url:
                            yield self.create_text_message(f"🔗 下载链接: {download_url}")
                            if download_video:
                                yield self.create_text_message("⬇️ 正在下载视频文件...")
                                try:
                                    video_response = requests.get(download_url, timeout=120)
                                except requests.exceptions.RequestException as e:
                                    yield self.create_text_message(
                                        f"❌ 视频下载失败: {str(e)}"
                                    )
                                    video_response = None

                                if video_response and video_response.status_code == 200:
                                    yield self.create_blob_message(
                                        blob=video_response.content,
                                        meta={
                                            "mime_type": "video/mp4",
                                            "filename": filename,
                                        },
                                    )
                                    yield self.create_text_message("✅ 视频下载完成")
                                elif video_response is not None:
                                    yield self.create_text_message(
                                        f"❌ 视频下载失败，状态码: {video_response.status_code}"
                                    )
                    elif file_response is not None:
                        yield self.create_text_message(
                            f"❌ 获取下载链接失败，状态码: {file_response.status_code}"
                        )

            result_json = {
                "task_id": resp_data.get("task_id"),
                "status": status,
                "file_id": file_id,
                "video_width": video_width,
                "video_height": video_height,
                "download_url": download_url,
                "base_resp": resp_data.get("base_resp"),
            }
            yield self.create_json_message(result_json)

            logger.info("Video query completed")

        except Exception as e:
            error_msg = f"❌ 查询视频结果时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
