import click
from tabulate import tabulate
import re
import sys
import os
import boto3
from dotenv import load_dotenv
import json
import questionary
from pipes.utils import get_or_create_pipes_session, token_valid, get_token, print_response, ClientSettings, get_cognito_access_token, token_valid
load_dotenv()


settings = ClientSettings()
TOKEN = get_token()

MAX_PROMPT = 3
cognito_idp = boto3.client("cognito-idp", region_name="us-west-2")


def validate_email_input(value):
    regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if not re.fullmatch(regex, value):
        print("Not a valid email address.")
        return None
    return value


@click.command()
def login():
    """Config session for CLI client"""
    # Change Output
    data = {}
    # Prompt for email
    for _ in range(MAX_PROMPT):
        input_value = questionary.text(
            "Email [Required]"
        ).ask()
        email = validate_email_input(input_value.strip())
        if email is None:
            continue
        data["email"] = email
        break
    if "email" not in data:
            response = {
                "code": "INVALID_ARGUMENT",
                "details": "Invalid email address! Failed to config your session"
            }
            print_response(response)
            sys.exit(1)

    # Prompt for password
    for _ in range(MAX_PROMPT):
        password = questionary.password(
            "Password [Required]"
        ).ask().strip()
        if password:
            data["password"] = password
            break
        else:
            print("Password cannot be empty.")
            continue
    if "password" not in data:
        response = {
            "code": "INVALID_ARGUMENT",
            "details": "Password is required! Failed to config your session"
        }
        print_response(response)
        sys.exit(1)
    session = get_or_create_pipes_session()
    email = data.get("email")
    password = data.pop("password")
    try:
        token = get_cognito_access_token(email, password)
        data["token"] = token
        session.update(data)
        session.save()
        print_response(f"Login success!")
    except cognito_idp.exceptions.NotAuthorizedException as e:
        token = session.data["token"]
        if not token_valid(token):
            print_response("Username and/or password is incorrect, and current session token is invalid")
        else:
            print_response("Current token is valid, but username and/or password is incorrect.")

