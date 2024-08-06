import click
import questionary
from pipes.utils import get_or_create_pipes_session, ClientSettings, print_response

MAX_PROMPT = 3


@click.group()
def config():
    """config CLI client"""


@config.command()
def server():
    """Config credentials for CLI client"""

    data = {}
    selected = questionary.select(
        "Choose the PIPES server:",
        choices=[
            "[production] pipes-api.nrel.gov:443",
            "[development] pipes-api-dev.nrel.gov:443",
            "[localhost] http://localhost:8080/",
        ]
    ).ask()
    pipes_server = selected.split("] ")[1]
    data["pipes_server"] = pipes_server

    settings = ClientSettings(**data)
    settings.save()


@config.command()
def show():
    """Gets session details and server endpoint"""
    session = get_or_create_pipes_session()
    settings = ClientSettings()

    # Collecting session data
    session_data = {
        "User Email": session.data["email"],
        "Session Token": f"{session.data['token'][0:6]}...{session.data['token'][-5:]}",
        "Server": settings.get_server()
    }
    print_response(session_data)
