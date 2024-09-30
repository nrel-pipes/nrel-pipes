import shutil

import click

from pipes.utils import print_response
from pipes.config import ClientConfig

from pipes.config import PIPES_CONFIG_DIR, PIPES_CONFIG_FILE, PIPES_CONFIG_FILE_DEFAULT


@click.group()
def config():
    """Config the PIPES client"""


@config.command()
def init():
    """Initialize the client configuration"""

    if not PIPES_CONFIG_DIR.exists():
        PIPES_CONFIG_DIR.mkdir(exist_ok=True)

    if not PIPES_CONFIG_FILE.exists():
        shutil.copyfile(PIPES_CONFIG_FILE_DEFAULT, PIPES_CONFIG_FILE)

    print("Config initialized successfully.")


@config.command()
def show():
    """Show the CLI client configuration"""
    config = ClientConfig()
    print_response(config.data)
