from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
import os
from .common import PIPES_SETTINGS_FILE


class ClientSettings(BaseSettings):
    """Settings for config cloud credentials"""
    pipes_server: str = Field(
        title="pipes_server",
        env="PIPES_SERVER",
        default=""
    )
    pipes_access_token: Optional[str] = Field(
        title="pipes_access_token",
        env="PIPES_ACCESS_TOKEN",
        default="",
    )
    pipes_id_token: Optional[str] = Field(
        title="pipes_id_token",
        env="PIPES_ID_TOKEN",
        default="",    
    )

    class Config:
        extra = "allow"
        case_sensitive = True
        env_file = PIPES_SETTINGS_FILE
        env_file_encoding = "utf-8"

    def save(self):
        with open(PIPES_SETTINGS_FILE, "w") as fw:
            for key, value in self.__dict__.items():
                fw.write(f"{key.upper()}={value}\n")

    def get(self):
        data = {}
        with open(PIPES_SETTINGS_FILE, "r") as fr:
            for line in fr:
                key, value = line.strip().split("=")
                data[key] = value
        return data
    
    def get_server(self):
        return self.get()["PIPES_SERVER"]