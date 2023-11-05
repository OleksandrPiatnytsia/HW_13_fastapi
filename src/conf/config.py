# from pydantic import BaseSettings
import pathlib

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# file_env = pathlib.Path(__file__).parent.parent.parent.joinpath(".env")


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_sender_name: str
    redis_host: str
    redis_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    # model_config = ConfigDict(env_file=file_env, env_file_encoding="utf-8")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = 'ignore'


config = Settings()
