import json
import sys
from pathlib import Path

from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings

PIPES_API_SERVER = 'pipes-api.nrel.gov'

PIPES_CONFIG_DIR = Path.home() / ".pipes"

PIPES_CONFIG_FILE = Path.home() / ".pipes" / "config"

PIPES_DEFAULT_CONFIG_FILE = Path(__file__).parent  / "config" / "default" / "config"

PIPES_COGNITO_CLIENT_ID = "6n5co9eh7bab4a21egr95ds3r8"


class ClientConfig(BaseSettings):
    """Settings for config cloud credentials"""
    pipes_server: str = Field(
        title="server",
        default=PIPES_API_SERVER,
    )
    pipes_cognito: str = Field(
        title="cognito",
        default=PIPES_COGNITO_CLIENT_ID
    )
    pipes_username: EmailStr | None = Field(
        title="username",
        default=None,
    )
    pipes_password: str | None = Field(
        title="password",
        default=None,
    )

    class Config:
        extra = "allow"
        case_sensitive = True
        env_file = PIPES_CONFIG_FILE
        env_file_encoding = "utf-8"

    @property
    def data(self):
        result = {}
        if not PIPES_CONFIG_FILE.exists():
            print("No config found, please run 'pipes config init'")
            sys.exit(1)

        with open(PIPES_CONFIG_FILE, "r") as fr:
            for line in fr:
                key, value = line.strip().split("=")
                result[key] = value
        return result

    def save(self):
        with open(PIPES_CONFIG_FILE, "w") as fw:
            for key, value in self.__dict__.items():
                fw.write(f"{key.lower()}='{value}'\n")
