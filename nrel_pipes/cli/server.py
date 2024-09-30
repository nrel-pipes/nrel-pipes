import sys

import click
import questionary

from nrel_pipes.utils import print_response
from nrel_pipes.config import ClientConfig, PIPES_CONFIG_DATA
from nrel_pipes.client.base import PipesClientBase


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
    """Show current PIPES server"""
    config = ClientConfig()
    print_response(config.pipes_server)


@server.command()
def conf():
    """Switch the PIPES server"""
    config = ClientConfig()
    selected = questionary.select(
        "Choose the PIPES server:",
        choices=[
            "[prod] https://pipes-api.nrel.gov",
            "[dev] https://pipes-api-dev.nrel.gov",
            "[local] http://localhost:8080",
        ]
    ).ask()
    if not selected:
        print(config)
        sys.exit(1)
    env = selected.split("] ")[0][1:]
    pipes_server = selected.split("] ")[1]

    if config.pipes_server != pipes_server:
        config.pipes_server = pipes_server
        config.pipes_cognito = PIPES_CONFIG_DATA[env]["PIPES_COGNITO_CLIENT"]
        config.save()
        print("! Server changed, please run 'pipes login' to login")
    else:
        print("! Server no change")
