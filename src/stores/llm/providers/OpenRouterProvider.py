from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
import requests
import logging

class OpenRouterProvider(LLMInterface):
    """
    Provider for OpenRouter API.
    """

    def __init__(self,
                 api_key: str,
                 api_url: str = "https://openrouter.ai/api/v1/chat/completions",
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):

        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.enums = OpenAIEnums

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [],
                      max_output_tokens: int = None,
                      temperature: float = None):

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenRouter was not set")
            return None

        max_output_tokens = max_output_tokens or self.default_generation_max_output_tokens
        temperature = temperature or self.default_generation_temperature

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.generation_model_id,
            "messages": chat_history + [{"role": "user", "content": self.process_text(prompt)}],
            "max_tokens": max_output_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                self.logger.error("No choices returned from OpenRouter")
                return None
        except Exception as e:
            self.logger.error(f"Error generating text via OpenRouter: {e}")
            return None

    def embed_text(self, text: str, document_type: str = None):
        """
        OpenRouter may not support embeddings directly.
        If it does, implement similarly to generate_text but using the embeddings endpoint.
        """
        self.logger.warning("Embedding via OpenRouter is not implemented.")
        return None
    
    def construct_prompt(self, prompt: str, role: str):
        return {"role": role, "content": self.process_text(prompt)}