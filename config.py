from pydantic_settings import BaseSettings
from pydantic import SecretStr, field_validator
from typing import List, Union


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DEBUG: bool = False
    ADMIN_IDS: Union[int, List[int]] = []
    RATE_LIMIT: int = 10

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str) and v:
            return [int(x.strip()) for x in v.split(",")]
        if isinstance(v, int):
            return [v]
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()


def get_bot_token() -> str:
    return settings.BOT_TOKEN.get_secret_value()