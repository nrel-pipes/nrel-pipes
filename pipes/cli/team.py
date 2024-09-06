import toml

import click
import requests

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.config import ClientConfig
from pipes.client import PipesClient
from pipes.template import load_template
from pipes.utils import print_response


@click.group()
@click.pass_context
def team(ctx):
    """Project operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="project short name"
)
def list(project_name):
    """List all teams under given project"""
    client = PipesClient()
    response = client.list_teams(project_name=project_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="project short name"
)
@click.option(
    "-t", "--team-name",
    type=str,
    required=True,
    help="team name"
)
def get(project_name, team_name):
    """Get one project team"""
    client = PipesClient()
    team = client.get_team(project_name, team_name)
    if not team:
        print(f"No team named '{team_name}' under project '{project_name}'")
        return
    print_response(team)


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="The project template path"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create(project_name, template_file):
    """Create new project team"""
    team_data = load_template(template_file)

    client = PipesClient()
    response = client.create_team(project_name, team_data)
    if response.status_code >= 500:
        print_response(response.text)
        return

    print_response(response.json())


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="The project template path"
)
@click.option(
    "-t", "--team-name",
    type=str,
    required=True,
    help="team name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=False,
    help="Template file"
)
def update(project_name, template_file):
    """Update team info and/or members"""
    team_data = load_template(template_file)

    client = PipesClient()
    response = client.update_team(project_name, team_data)
    if response.status_code >= 500:
        print_response(response.text)
        return

    print_response(response.json())
