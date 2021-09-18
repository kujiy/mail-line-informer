from pydantic import BaseSettings


class Env(BaseSettings):
    LINE_BASE_TOKEN: str = 'test'
    LINE_TOKEN_WAGAYA: str = 'test'

    MAIL_HOST: str = 'test'
    MAIL_USER: str = 'test'
    MAIL_PASSWORD: str = 'test'
    MAIL_BOX: str = 'test'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


env = Env()
