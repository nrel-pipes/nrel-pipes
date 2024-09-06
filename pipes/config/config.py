import sys
from pathlib import Path

from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings

PIPES_CONFIG_DIR = Path.home() / ".pipes"

PIPES_CONFIG_FILE = Path.home() / ".pipes" / "config"

PIPES_CONFIG_FILE_DEFAULT = Path(__file__).parent  / "config" / "default" / "config"

PIPES_CONFIG_DATA = {
    "local": {
        "PIPES_API_SERVER": "http://127.0.0.1:8080",
        "PIPES_COGNITO_CLIENT": "6n5co9eh7bab4a21egr95ds3r8"
    },
    "dev": {
        "PIPES_API_SERVER": "https://pipes-api-dev.nrel.gov",
        "PIPES_COGNITO_CLIENT": "clfpli1avt6eil03ovr11qdpi"
    },
    "prod": {
        "PIPES_API_SERVER": "https://pipes-api.nrel.gov",
        "PIPES_COGNITO_CLIENT": "539o71b6rh0ua124ro8q3bv39s"
    }
}


class ClientConfig(BaseSettings):
    """Settings for config cloud credentials"""
    pipes_server: str = Field(
        title="server",
        default=PIPES_CONFIG_DATA["prod"]["PIPES_API_SERVER"],
    )
    pipes_cognito: str = Field(
        title="cognito",
        default=PIPES_CONFIG_DATA["prod"]["PIPES_COGNITO_CLIENT"]
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
