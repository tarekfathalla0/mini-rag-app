from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging


class AzureOpenAIProvider(LLMInterface):
    """
    Azure OpenAI Provider
    - يستخدم Azure OpenAI deployments لتوليد النصوص أو استخراج embeddings
    - يتم تحديد Deployment Names لاحقًا عبر set_generation_model و set_embedding_model
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        api_version: str = "2023-07-01-preview",
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")  # تأكد من إزالة أي / إضافية
        self.api_version = api_version

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_deployment_name = None
        self.embedding_deployment_name = None
        self.embedding_size = None

        # Azure OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=f"{self.endpoint}/openai/deployments",
            default_query={"api-version": self.api_version},
        )

        self.logger = logging.getLogger(__name__)

    # ====== Setters ======
    def set_generation_model(self, deployment_name: str):
        """تعيين اسم الـ Azure deployment الخاص بالـ generation"""
        self.generation_deployment_name = deployment_name

    def set_embedding_model(self, deployment_name: str, embedding_size: int):
        """تعيين اسم الـ Azure deployment الخاص بالـ embeddings"""
        self.embedding_deployment_name = deployment_name
        self.embedding_size = embedding_size

    # ====== Core Methods ======
    def process_text(self, text: str) -> str:
        return text[: self.default_input_max_characters].strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list = None,
        max_output_tokens: int = None,
        temperature: float = None,
    ):
        chat_history = chat_history or []

        if not self.client:
            self.logger.error("Azure OpenAI client is not initialized.")
            return None
        if not self.generation_deployment_name:
            self.logger.error("Generation deployment name not set for Azure OpenAI.")
            return None

        max_output_tokens = max_output_tokens or self.default_generation_max_output_tokens
        temperature = temperature or self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.generation_deployment_name,
                messages=chat_history,
                max_tokens=max_output_tokens,
                temperature=temperature,
            )

            if (
                not response
                or not getattr(response, "choices", None)
                or len(response.choices) == 0
                or not getattr(response.choices[0], "message", None)
            ):
                self.logger.error("Azure OpenAI returned an empty response.")
                return None

            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error generating text via Azure OpenAI: {e}")
            return None

    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Azure OpenAI client is not initialized.")
            return None
        if not self.embedding_deployment_name:
            self.logger.error("Embedding deployment name not set for Azure OpenAI.")
            return None

        try:
            response = self.client.embeddings.create(
                model=self.embedding_deployment_name,
                input=text,
            )
            if (
                not response
                or not getattr(response, "data", None)
                or len(response.data) == 0
                or not getattr(response.data[0], "embedding", None)
            ):
                self.logger.error("Azure OpenAI embedding returned empty result.")
                return None

            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error embedding text via Azure OpenAI: {e}")
            return None

    def construct_prompt(self, prompt: str, role: str):
        return {"role": role, "content": self.process_text(prompt)}
