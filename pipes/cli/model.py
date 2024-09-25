import click

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template
from pipes.client import PipesClient
from pipes.utils import print_response


@click.group()
@click.pass_context
def model(ctx):
    """Model operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@model.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=True,
    help="The project name"
)
@click.option(
    "-r", "--projectrun-name",
    type=click.STRING,
    required=False,
    help="The projectrun name"
)
def list(project_name, projectrun_name):
    """List all models under a project run"""
    client = PipesClient()
    response = client.list_models(project_name, projectrun_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@model.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=False,
    help="The project name"
)
@click.option(
    "-r", "--projectrun-name",
    type=click.STRING,
    required=False,
    help="The projectrun name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create(project_name, projectrun_name, template_file):
    """Create new model from template"""
    data = load_template(template_file)
    client = PipesClient()
    response = client.create_models(project_name, projectrun_name, data)
    print_response(response)


# @model.command()
# @click.option(
#     "-p", "--project-name",
#     type=click.STRING,
#     required=True,
#     help="The project name"
# )
# @click.option(
#     "-r", "--projectrun-name",
#     type=click.STRING,
#     required=True,
#     help="The projectrun name"
# )
# @click.option(
#     "-m", "--model-name",
#     type=click.STRING,
#     required=True,
#     help="The model name"
# )
# def progress(project_name, projectrun_name, model_name):
#     """Check the model progress"""
#     client = PipesClient()
#     response = client.check_model_progress(project_name, projectrun_name, model_name)
#     print_response(response)
