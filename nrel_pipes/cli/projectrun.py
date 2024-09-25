import sys

import click

from nrel_pipes.auth import validate_session_token
from nrel_pipes.cli.login import login
from nrel_pipes.client import PipesClient
from nrel_pipes.session import Session
from nrel_pipes.template import load_template
from nrel_pipes.utils import print_response


from nrel_pipes.config import ClientConfig


@click.group()
@click.pass_context
def projectrun(ctx):
    """Project run operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@projectrun.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="The project name"
)
def list(project_name):
    """List all available project runs"""
    session = Session()

    if not project_name:
        if session.contains("project"):
            _project = session.get("project")
            project_name = _project["name"]

    if not project_name:
        print("No project cache found, project name is required.")
        sys.exit(1)

    client = PipesClient()
    response = client.list_projectruns(project_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@projectrun.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="Name of project"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create(project_name, template_file):
    """Create one or multiple project runs"""
    data = load_template(template_file)
    client = PipesClient()
    response = client.create_projectruns(project_name, data)
    print_response(response)
