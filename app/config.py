from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_port: str
    db_name: str
    db_user: str
    password: str
    db_host: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env')


setting = Settings()
    

