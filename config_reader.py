from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """
    The Settings class manages the settings of private data.

    :param bot_token:  Bot token
    :param api_key:    API key
    :param secret_key: Secret key
    """
    bot_token: SecretStr
    api_key: SecretStr
    secret_key: SecretStr

    class Config:
        """
        The Config class sets the configuration for reading data from the .env file.

        :param env_file:          Path to the .env file
        :param env_file_encoding: Encoding of the .env file
        """
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
