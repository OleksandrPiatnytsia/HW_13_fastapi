# from pydantic import BaseSettings
import pathlib

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# file_env = pathlib.Path(__file__).parent.parent.parent.joinpath(".env")


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql://user:password@localhost/dbname"
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    mail_username: str = "username@test.com"
    mail_password: str = "password"
    mail_from: str = "username@test.com"
    mail_port: int = 465
    mail_server: str = "localhost"
    mail_sender_name: str = "username"
    redis_host: str = "localhost"
    redis_port: int = 2032
    cloudinary_name: str = "cloudinary_name"
    cloudinary_api_key: str = "cloudinary_api_key"
    cloudinary_api_secret: str = "cloudinary_api_secret"

    # model_config = ConfigDict(env_file=file_env, env_file_encoding="utf-8")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = 'ignore'


config = Settings()
