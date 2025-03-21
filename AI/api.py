from django.conf import settings
from django.core.files.storage import default_storage
import requests
import json
from markdownify import markdownify as md

import re


class DeepSeekAPI:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get_response(self, message):
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            "stream": False,
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            ai_message = (
                response_data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response received.")
            )

            return ai_message

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from API."
