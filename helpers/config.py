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
    class Config:
        env_file = ".env"
def get_settings():
    return Settings()
