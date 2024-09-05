import click

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template
from pipes.client import PipesClient
from pipes.utils import print_response



@click.group()
@click.pass_context
def user(ctx):
    """User operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@user.command()
def list():
    """List all users"""
    client = PipesClient()
    response = client.list_users()
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@user.command()
@click.option(
    '-u', '--username',
    type=str,
    required=False,
    help="Username is an email address"
)
def get(username):
    """Get user by email address"""
    client = PipesClient()
    response = client.get_user(username)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@user.command()
@click.option(
    "-u", "--username",
    type=str,
    required=False,
    help="Username is an email address"
)
@click.option(
    "-f", "--first-name",
    type=str,
    default=None,
    help="First name of this user"
)
@click.option(
    "-l", "--last-name",
    type=str,
    default=None,
    help="Last name of this user"
)
@click.option(
    "-o", "--orgnization",
    type=str,
    default=None,
    help="Orgnization name of this user"
)
def create(username, first_name, last_name, orgnization):
    """Create a new user"""
    data = {
        "email": username,
        "first_name": first_name,
        "last_name": last_name,
        "orgnization": orgnization
    }
    client = PipesClient()
    response = client.create_user(data)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())
