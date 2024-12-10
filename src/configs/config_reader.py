import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    secret_key: SecretStr
    
    # Для проверки API ключей
    url: str = 'https://api-key.fusionbrain.ai/'
    
    # Стили генерации
    styles: list = [
        'KANDINSKY',
        'DEFAULT',
        'ANIME'
    ]

    model_config = SettingsConfigDict(env_file=f"{pathlib.Path(__file__).resolve().parent}/config.env",
                                      env_file_encoding='utf-8')


cfg = Settings()