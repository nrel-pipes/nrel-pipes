import click
import sys

import questionary

from pipes.auth import initiate_auth
from pipes.config import ClientConfig
from pipes.session import Session
from pipes.utils import validate_email_input


MAX_PROMPT = 3


@click.command()
def login():
    """Login to PIPES API server"""
    data = {}

    config = ClientConfig()
    username = config.pipes_username
    password = config.pipes_password

    yes = False
    if username:
        yes = questionary.confirm("Username(Email): " + username).ask()
        if yes is None:
            sys.exit(1)

    if (yes is False) or (not username):
        # Prompt for username(email)
        for _ in range(MAX_PROMPT):
            input_value = questionary.text(
                "Username(Email):"
            ).ask()
            if not input_value:
                break

            username = validate_email_input(input_value.strip())
            if username is None:
                continue
            data["username"] = username
            break
        if "username" not in data:
            print("Login failed, invalid email address!")
            sys.exit(1)
        username = data.get("username")
        config.pipes_username = username

    # Prompt for password
    for _ in range(MAX_PROMPT):
        password = questionary.password(
            "Password:"
        ).ask()
        if password:
            data["password"] = password.strip()
            break
        else:
            break
    if "password" not in data:
        print("Login failed, no password input.")
        sys.exit(1)
    password = data.pop("password")
    config.pipes_password = password

    # Login for getting access token
    session = Session()
    try:
        token = initiate_auth(username, password)
        data["token"] = token
        session.update(data)
        session.save()
        config.save()
        print(f"Login success! {config.pipes_server}")
    except Exception:
        print("Incorrect username and/or password, please try again.")
