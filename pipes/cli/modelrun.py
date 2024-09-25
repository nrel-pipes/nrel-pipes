import click

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template
from pipes.client import PipesClient
from pipes.utils import print_response, prompt_overwrite


@click.group()
@click.pass_context
def modelrun(ctx):
    """Model run operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@modelrun.command()
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
    help="The project run name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=False,
    help="The project run name"
)
def list(project_name, projectrun_name, model_name):
    """List all available model runs"""
    client = PipesClient()
    response = client.list_modelruns(project_name, projectrun_name, model_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@modelrun.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=True,
    help="The project name"
)
@click.option(
    "-r", "--projectrun-name",
    type=click.STRING,
    required=True,
    help="The projectrun name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The project run name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The model run template path"
)
def create(project_name, projectrun_name, model_name, template_file):
    """Create model run from template"""
    modelruns_data = load_template(template_file)
    client = PipesClient()
    response = client.create_modelrun(project_name, projectrun_name, model_name, modelruns_data)
    print_response(response)
