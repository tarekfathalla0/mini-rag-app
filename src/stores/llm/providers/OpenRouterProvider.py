from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum
import requests
import logging
import json


class OpenRouterProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
        site_url: str = None,
        site_title: str = None
    ):
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.site_url = site_url
        self.site_title = site_title

        self.logger = logging.getLogger(__name__)

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(
        self,
        prompt: str,
        max_output_tokens: int = None,
        chat_history: list = [],
        temperature: float = None
    ):
        if not self.api_key:
            self.logger.error("OpenRouter API key not set.")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model ID not set.")
            return None

        max_output_tokens = (
            max_output_tokens
            if max_output_tokens
            else self.default_generation_max_output_tokens
        )

        temperature = (
            temperature
            if temperature is not None
            else self.default_generation_temperature
        )

        messages = []

        for msg in chat_history:
            messages.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })

        messages.append({
            "role": "user",
            "content": self.process_text(prompt)
        })

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        if self.site_url:
            headers["HTTP-Referer"] = self.site_url

        if self.site_title:
            headers["X-Title"] = self.site_title

        payload = {
            "model": self.generation_model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_output_tokens
        }

        response = requests.post(
            url=self.base_url,
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            self.logger.error(
                f"OpenRouter API error: {response.status_code} - {response.text}"
            )
            return None

        data = response.json()

        if (
            not data
            or "choices" not in data
            or not data["choices"]
            or "message" not in data["choices"][0]
        ):
            self.logger.error("Invalid response from OpenRouter API.")
            return None

        return data["choices"][0]["message"]["content"]

    def embed_text(self, text: str, document_type: str = None):
        self.logger.error(
            "OpenRouter does not provide a unified embeddings API."
        )
        return None

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
