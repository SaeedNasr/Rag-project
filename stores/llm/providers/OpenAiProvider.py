from ..LLMinterface import LLMInterface 
from openai import OpenAI
import logging
from ..LLMenums import OpenAiEnum
class OpenAiProvider(LLMInterface):
    def __init__(self,api_key:str,api_url:str=None,
                 default_input_max_characters:int=1000,
                 default_output_max_tokens:int=1000,
                 temperature:float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.temperature = temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embeddings_size = None 

        self.client = OpenAI(api_key=self.api_key, api_url=self.api_url)

        self.logger = logging.getLogger(__name__)

    def process_text(self, text:str):
        return text[:self.default_input_max_characters].strip()

    def get_generation_model(self, model_id:str):
        self.generation_model_id = model_id
        #to be able to change model on the fly if needed

    def get_embedding_model(self, model_id:str,embedding_size:int):
        self.embedding_model_id = model_id
        self.embeddings_size = embedding_size

    def construct_prompt(self, prompt:str,role:str):
        return {
            "role" : role,
            "prompt": self.process_text(prompt)
        }
    
    def generate_text(self, prompt:str,chat_history:list = [],max_output_tokens:int = None, temperature:float = None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID for OpenAI is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.temperature

        chat_history = chat_history.append(self.construct_prompt(prompt=prompt,role=OpenAiEnum.USER.value))

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("An error while generating text with OpenAi")

        return response.choices[0].message["content"]

    def embed_text(self, text:str,document_type:str  = None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        
        response = self.client.embeddings.create(model = self.embedding_model_id,
                                                    input = text)
        
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embeddings:
            self.logger.error("An error while embedding text with OpenAi")
            return None 
        
        return response.data[0].embeddings


