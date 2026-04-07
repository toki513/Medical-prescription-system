from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
        DATABASE_URL:str
        SECRET_KEY:str
        ALGORITHM:str =  "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
        APP_NAME:str= "Medical Prescription API"
        DEBUG:bool = True
        
        model_config=SettingsConfigDict(env_file=".env")
    
settings = Settings()