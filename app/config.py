from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
        DATABASE_URL:str
        SECRET_KEY:SecretStr
        ALGORITHM:str =  "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
        APP_NAME:str= "Medical Prescription API"
        DEBUG:bool = True
        
        class config:
                env_file=".env"
        
    
settings = Settings()