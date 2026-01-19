from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str 
    API_KEY: str 
    FILE_ALLOWED_TYPES: list 
    MAX_FILE_SIZE_MB: int 
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_DB_URI : str
    MONGO_DB_NAME: str

    

    OPENAI_API_KEY :str = None
    OPENAI_API_URL :str = None
    COHERE_API_KEY :str = None

    GENERATION_BACKEND :str
    EMBEDDING_BACKEND :str

    GENERATION_MODEL_ID :str = None
    EMBEDING_MODEL_ID :str = None
    EMBEDING_MODEL_SIZE : int = None

    INPUT_DEFALUT_MAX_CHARACTERS :int = None
    GENERATION_DEFAULT_MAX_TOKENS :int = None
    GENERATION_DEFAULT_TEMPRATURE :float = None
    
    class Config:
        env_file = ".env"
def get_settings():
    return Settings()
