from .LLMenums import LLMEnum
from .providers import OpenAiProvider ,CoHereProvider

class LLMProviderFactory:
    def __init__(self,config:dict):
        self.config = config

    def create(self,provider:str):
        if provider == LLMEnum.OPENAI.value:
            return OpenAiProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters = self.config.INPUT_DEFALUT_MAX_CHARACTERS,
                default_output_max_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                temprature = self.config.GENERATION_DEFAULT_TEMPRATURE
            )
        elif provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFALUT_MAX_CHARACTERS,
                default_output_max_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                temprature = self.config.GENERATION_DEFAULT_TEMPRATURE
            )
        return None