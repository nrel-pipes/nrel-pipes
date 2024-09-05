import click

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template
from pipes.client import PipesClient
from pipes.utils import print_response


@click.group()
@click.pass_context
def project(ctx):
    """Project operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@project.command()
def list():
    """List all available projects"""
    client = PipesClient()
    response = client.list_projects()
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@project.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=False,
    help="The project name in unique"
)
@click.option(
    "--owner",
    is_flag=True,
    help="Filter project owner"
)
def get(project_name, owner):
    """Get given project metadata"""
    session = Session()

    project = None
    if session.contains("project"):
        _project = session.get("project")
        if _project["name"] == project_name:
            project = _project

    if not project:
        client = PipesClient()
        response = client.get_project(name=project_name)

        if response.status_code >= 500:
            print_response(response.text)
            return

        if response.status_code == 200:
            project = response.json()
            session.update({"project": project})
        else:
            print_response(response.json())
            return

    if owner:
        print_response(project["owner"])
        return

    print_response(project)


@project.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template file"
)
def create(template_file):
    """Create project from template"""
    data = load_template(template_file)
    client = PipesClient()
    response = client.create_project(data)
    print_response(response)
