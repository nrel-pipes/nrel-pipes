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
from pipes.client import PipesClientBase
from utils.common import PIPES_CLIENT_ID
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


def load_json(filename):
    file = open(filename, "r")
    data = json.loads(file.read())
    return data


def get_cognito_access_token(username, password):
    """Get Cognit access token for Bearer authentication"""
    response = cognito_idp.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
        ClientId=PIPES_CLIENT_ID,
    )
    access_token = response["AuthenticationResult"]["AccessToken"]
    return access_token


@click.group()
def service(args=None):
    """system operation commands"""


@service.command()
@click.pass_context
def ping(ctx):
    """PIPES server health check"""
    client = PipesClientBase(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.check_connection()
    print_response(response.json())


# @click.command()
# def login():
#     """Config session for CLI client"""
#     # Change Output
#     data = {}
#     # Prompt for email
#     for _ in range(MAX_PROMPT):
#         input_value = questionary.text(
#             "Email [Required]"
#         ).ask()
#         email = validate_email_input(input_value.strip())
#         if email is None:
#             continue
#         data["email"] = email
#         break
#     if "email" not in data:
#             response = {
#                 "code": "INVALID_ARGUMENT",
#                 "details": "Invalid email address! Failed to config your session"
#             }
#             print_response(response)
#             sys.exit(1)

#     # Prompt for password
#     for _ in range(MAX_PROMPT):
#         password = questionary.password(
#             "Password [Required]"
#         ).ask().strip()
#         if password:
#             data["password"] = password
#             break
#         else:
#             print("Password cannot be empty.")
#             continue
#     if "password" not in data:
#         response = {
#             "code": "INVALID_ARGUMENT",
#             "details": "Password is required! Failed to config your session"
#         }
#         print_response(response)
#         sys.exit(1)
#     session = get_or_create_pipes_session()
#     email = data.get("email")
#     password = data.pop("password")
#     try:
#         token = get_cognito_access_token(email, password)
#         data["token"] = token
#         session.update(data)
#         session.save()
#         print_response(f"Login success!")
#     except cognito_idp.exceptions.NotAuthorizedException as e:
#         token = session.data["token"]
#         if not token_valid(token):
#             print_response("Username and/or password is incorrect, and current session token is invalid")
#         else:
#             print_response("Current token is valid, but username and/or password is incorrect.")


def prompt_for_session():
    click.clear()

    session = get_or_create_pipes_session()
    project_runs_context = session.data['user_context']
    click.secho(f"Wecome to PIPES {session.data['username']}.")
    click.secho(f"You are currently active in the following project runs:")

    count = 0
    output_data = []
    for run in project_runs_context:
        count+=1
        output_data.append([count,  run['project']['data']['name'], '', '',run['project']['data']['scheduled_start'],run['project']['data']['scheduled_end'] ])
        output_data.append(['' , '', run['project_run']['data']['name'], '', run['project_run']['data']['scheduled_start'],run['project_run']['data']['scheduled_end'] ])
        for model in run["models"]:
            output_data.append(['','','',model['data']['model'],model['data']['scheduled_start'],model['data']['scheduled_end']])

        output_data.append(['-----------','-----------','-----------','-----------','-----------','-----------'])

    click.secho(tabulate(output_data, headers=["Selection #", "Project", "Project Run",  "Model", "Start Data", "End Date" ]), fg="blue")

    selected_run_number = click.prompt(f"Please select a Selection # from 1 to {count} for this session", type=int)
    if selected_run_number > count:
        click.clear()
        click.secho("Invalid selection.", fg='red')
        prompt_for_session()
    selected_run_number -= 1
    run_info = dict(selected_user_context=selected_run_number)
    session.update(run_info)
    session.save()


@service.command()
@click.option(
    "-f", "--first-name",
    type=click.STRING,
    help="The first name"
)
@click.option(
    "-l", "--last-name",
    type=click.STRING,
    help="The last name"
)
@click.option(
    "-e", "--email",
    type=click.STRING,
    help="The email address"
)
@click.option(
    "-o", "--organization",
    type=click.STRING,
    default=None,
    help="The organization name"
)
@click.pass_context
def add_user(ctx, first_name, last_name, email, organization):
    """Add a new user into PIPES"""
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "organization": organization
    }
    client = PipesClientBase(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.post_user(**data)
    if response.status_code == 201:
        print_response("User added successfully added.")
    else:
        print_response(f"Could not add user. Error message: {response.json()}")

@click.option(
    "-p", "--project",
    type=click.STRING,
    default=None,
    required=True,
    help="The project name"
)
@service.command()
@click.pass_context
def list_modeling_teams(ctx, project):
    """List the modeling teams in PIPES"""
    client = PipesClientBase(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.get_teams(project)
    if response.status_code == 200:
        print_response(response.json())
    else:
        print_response(f"Could not get project. Error message: {response.json()}")
