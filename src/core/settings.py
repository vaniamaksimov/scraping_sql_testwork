from abc import ABC

from pydantic import BaseModel, BaseSettings, Field, PostgresDsn, SecretStr, validator


class ABCSettings(BaseSettings, ABC):
    class Config(BaseSettings.Config):
        env_file = '.env'


class DbSettings(ABCSettings):
    scheme: str = Field(..., env='POSTGRES_SCHEME')
    user: str = Field(..., env='POSTGRES_USER')
    password: SecretStr = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')
    db: str = Field(
        ...,
        env='POSTGRES_DB',
    )
    url: str | PostgresDsn = Field(None, env='DATABASE_URL')

    @validator('url')
    def url_validator(cls, value: str | PostgresDsn | None, values: dict[str, str]):
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme=values.get('scheme'),
            user=values.get('user'),
            password=values.get('password').get_secret_value(),
            host=values.get('host'),
            port=str(values.get('port')),
            path=f'/{values.get("db") or ""}',
        )

    class Config(ABCSettings.Config):
        ...


class AppSettings(ABCSettings):
    max_string_length: int = 255

    class Config(ABCSettings.Config):
        ...


class Settings(BaseModel):
    db: DbSettings = DbSettings()
    app: AppSettings = AppSettings()


settings = Settings()
