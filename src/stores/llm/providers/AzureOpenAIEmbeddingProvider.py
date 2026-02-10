from openai import AzureOpenAI
import logging
from ..LLMInterface import LLMInterface

class AzureOpenAIEmbeddingProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        azure_endpoint: str,
        api_version: str = "2024-02-15-preview",
        default_input_max_characters: int = 8000
    ):
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )

        self.default_input_max_characters = default_input_max_characters

        self.embedding_model_id = None
        self.embedding_size = None

        self.logger = logging.getLogger(__name__)

    def set_embedding_model(self, deployment_name: str, embedding_size: int):
        self.embedding_model_id = deployment_name
        self.embedding_size = embedding_size

    def process_text(self, text: str) -> str:
        return text[:self.default_input_max_characters].strip()

    def embed_text(self, text: str):

        if not self.embedding_model_id:
            self.logger.error("Embedding model deployment not set.")
            return None

        processed_text = self.process_text(text)

        response = self.client.embeddings.create(
            model=self.embedding_model_id,  # Azure deployment name
            input=processed_text
        )

        if not response or not response.data:
            self.logger.error("No embedding returned from Azure OpenAI.")
            return None

        return response.data[0].embedding
