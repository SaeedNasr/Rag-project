from ..LLMinterface import LLMInterface 
import logging
from ..LLMenums import CoHereEnum , DocumentTypeEnum
import cohere

class CoHereProvider(LLMInterface):
    def __init__(self,api_key:str,
                 default_input_max_characters:int=1000,
                 default_output_max_tokens:int=1000,
                 temperature:float=0.1):
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.temperature = temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embeddings_size = 384 

        self.client = cohere.Client(api_key = self.api_key)

        self.logger = logging.getLogger(__name__)
        self.enums = CoHereEnum
    def process_text(self, text:str):
        return text[:self.default_input_max_characters].strip()

    def get_generation_model(self, model_id:str):
        self.generation_model_id = model_id
        #to be able to change model on the fly if needed

    def get_embedding_model(self, model_id:str,embeddings_size:int):
        self.embedding_model_id = model_id
        self.embeddings_size = embeddings_size


    def generate_text(self, prompt:str,chat_history:list = [],max_output_tokens:int = None, temperature:float = None):

        if not self.client :
            self.logger.error("Cohere client has not been initialized")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model ID for Cohere is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response:
            return None

        try:
            # 1. Try standard 'text' attribute (Cohere SDK V1/V2 standard)
            if hasattr(response, 'text') and response.text:
                return response.text
            
            # 2. Try the nested V2 'message' structure
            if hasattr(response, 'message'):
                content = response.message.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text
                return str(content)
                
            return str(response)
        except Exception as e:
            self.logger.error(f"Failed to parse Cohere response: {e}")
            return "Error parsing response."
            
      
    def construct_prompt(self, prompt:str,role:str):
        return {
            "role" : role,
            "text": self.process_text(prompt)
        }
    

    def embed_text(self, texts:str,document_type:str  = None):
        if not self.client :
            self.logger.error("Cohere client has not been initialized")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID for Cohere is not set.")
            return None
        
        input_type = CoHereEnum.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnum.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [self.process_text(texts)],
            input_type = input_type,
            embedding_types = ['float'] 
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while emmbeding with CoHere!")
            return None
        return response.embeddings.float[0]