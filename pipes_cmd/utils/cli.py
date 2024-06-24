import os
import click
import sys
import requests
from pipes_cmd.config.session import get_or_create_pipes_session
from pipes_cmd.config.settings import ClientSettings
# from pipes_sdk import PipesClient


def prompt_overwrite(ctx, param, value):
    """Callback to prompt the user to confirm if the CLI should overwrite the
    file."""

    if os.path.exists(value):
        click.confirm(f"File exists at '{value}'. Overwrite?", abort=True)

    return value


def get_selected_user_context_from_session():
    session = get_or_create_pipes_session()
    settings = ClientSettings()
    print("Data Sessions", session.data["token"])
    request = requests.get(
        url = f"{settings.pipes_server}",
        headers = {"Authorizations": f"Bearer {session.data["token"]}"}
        )
    
    print(f"Checking: {selected_user_context}, Request: {request}")
    if selected_user_context['code'] != 'OK':
        selected = {}
    else:
        selected = selected_user_context['data']

    if "project" not in selected:
        print("No project session found, please run 'pipes login' to fetch, or provide '-p/--project-name' option.")
        sys.exit(1)

    return selected
