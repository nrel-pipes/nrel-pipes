import click
import os
import sys

from nrel_pipes.cli.login import login
from nrel_pipes.auth import validate_session_token
from nrel_pipes.session import Session

from nrel_pipes.template import load_template, copy_template
from nrel_pipes.client import PipesClient
from nrel_pipes.utils import print_response, prompt_overwrite


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
        response = client.get_project(project_name=project_name)

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
    print_response(response["detail"])


@project.command()
@click.option(
    "-t", "--type-name",
    type=click.Choice([
        'project-creation',
    ]),
    required=True,
    help="Choose a template type"
)
@click.option(
    "-o", "--output-file",
    type=click.Path(),
    default=None,
    help="Output template path",
    callback=prompt_overwrite
)
def template(type_name, output_file):
    """Get project related template"""
    if not output_file:
        output_file = type_name + ".toml"

    _, ext = os.path.splitext(output_file)
    if not ext or "toml" not in ext.lower():
        print("Only .toml file is support as output")
        sys.exit(1)

    copy_to_dir = os.path.dirname(output_file)
    if copy_to_dir and not os.path.exists(copy_to_dir):
        os.makedirs(copy_to_dir, exist_ok=True)

    copy_template(type_name, output_file)

    print(f"Template generated: {output_file}")
