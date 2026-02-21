"""Provider validation for MiniMax Hailuo AIGC."""

# author: sawyer-shi

from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class HailuoAigcProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError("MiniMax API key is required")
            self._test_minimax_connection(api_key)
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"MiniMax API credential validation failed: {str(e)}"
            )

    def _test_minimax_connection(self, api_key: str) -> None:
        url = "https://api.minimaxi.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": "MiniMax-M2.5",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        except requests.RequestException as req_err:
            raise ToolProviderCredentialValidationError(
                f"Unable to reach MiniMax service: {req_err}"
            )

        if response.status_code != 200:
            try:
                data = response.json()
                error_message = (
                    data.get("error", {}).get("message")
                    or data.get("message")
                    or response.text
                )
            except Exception:
                error_message = response.text
            raise ToolProviderCredentialValidationError(
                f"MiniMax API error {response.status_code}: {error_message}"
            )

        try:
            data = response.json()
        except ValueError:
            raise ToolProviderCredentialValidationError(
                "MiniMax API returned non-JSON response"
            )

        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) == 0:
            raise ToolProviderCredentialValidationError(
                "MiniMax API response missing valid choices"
            )
