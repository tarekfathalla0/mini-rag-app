from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider, AzureOpenAIProvider, OpenRouterProvider

class LLMProviderFactory:
    def __init__(self, config):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        if provider == LLMEnums.AZURE.value:
            azure_client = AzureOpenAIProvider(
                api_key=self.config.AZURE_OPENAI_API_KEY,
                endpoint=self.config.AZURE_OPENAI_ENDPOINT,
                api_version=self.config.AZURE_OPENAI_API_VERSION,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

            if getattr(self.config, "AZURE_GENERATION_DEPLOYMENT_NAME", None):
                azure_client.set_generation_model(self.config.AZURE_GENERATION_DEPLOYMENT_NAME)

            if getattr(self.config, "AZURE_EMBEDDING_DEPLOYMENT_NAME", None):
                azure_client.set_embedding_model(
                    self.config.AZURE_EMBEDDING_DEPLOYMENT_NAME,
                    getattr(self.config, "EMBEDDING_MODEL_SIZE", None)
                )

            return azure_client

        if provider == LLMEnums.OPENROUTER.value:
            openrouter_client = OpenRouterProvider(
                api_key=self.config.OPENROUTER_API_KEY,
                api_url=getattr(self.config, "OPENROUTER_API_URL", None),
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

            if getattr(self.config, "OPENROUTER_MODEL_ID", None):
                openrouter_client.set_generation_model(self.config.OPENROUTER_MODEL_ID)

            # ملاحظة: OpenRouter غالبًا لا يدعم embeddings مباشرة، فمش بنحددها هنا
            return openrouter_client

        return None
