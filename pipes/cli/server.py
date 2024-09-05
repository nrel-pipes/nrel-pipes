import sys

import click
import questionary

from pipes.utils import print_response
from pipes.config import ClientConfig
from pipes.client.base import PipesClientBase


@click.group()
def server():
    """Server operation commands"""


@server.command()
def ping():
    """Check PIPES server availability"""
    client = PipesClientBase()
    response = client.ping()
    print_response(response)


@server.command()
def show():
    """Show current PIPES server host"""
    config = ClientConfig()
    print_response(config.pipes_server)


@server.command()
def update():
    config = ClientConfig()
    selected = questionary.select(
        "Choose the PIPES server:",
        choices=[
            "[production] https://pipes-api.nrel.gov",
            "[development] https://pipes-api-dev.nrel.gov",
            "[localhost] http://localhost:8080",
        ]
    ).ask()
    if not selected:
        print(config)
        sys.exit(1)
    pipes_server = selected.split("] ")[1]
    config.pipes_server = pipes_server
    config.save()
