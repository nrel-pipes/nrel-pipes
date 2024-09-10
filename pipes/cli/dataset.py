import click

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template
from pipes.client import PipesClient
from pipes.utils import print_response


@click.group()
@click.pass_context
def dataset(ctx):
    """Dataset operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@dataset.command()
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
    help="The model name"
)
@click.option(
    "-x", "--modelrun-name",
    type=click.STRING,
    required=True,
    help="The modelrun name"
)
def list(project_name, projectrun_name, model_name, modelrun_name):
    """List all available datasets"""
    client = PipesClient()
    response = client.list_datasets(project_name, projectrun_name, model_name, modelrun_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@dataset.command()
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
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The dataset template path"
)
@click.option(
    "--metadata-validation/--no-metadata-validation",
    default=True,
    is_flag=True,
    help="Whether to run metadata validation"
)
@click.option(
    "--adhoc",
    default=False,
    is_flag=True,
    help="Whether to run metadata validation"
)
def checkin(project_name, project_run_name, model_name, model_run_name, template_file, metadata_validation, adhoc):
    """Checkin new dataset"""
    dataset_data = load_template(template_file)
    client = PipesClient()
    response = client.checkin_dataset(project_name, project_run_name, model_name, model_run_name, dataset_data, adhoc)
    if response.status_code == 201:
        print_response("Dataset successfully checked in.")
    else:
        print_response(f"Encountered error: {response}")


@dataset.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=False,
    help="The project name"
)
@click.option(
    "-r", "--project-run-name",

    type=click.STRING,
    required=False,
    help="The project run name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-d", "--dataset-name",
    type=click.STRING,
    required=True,
    help="The dataset name"
)
def location(ctx, project_name, project_run_name, model_name, model_run_name, dataset_name):
    """Get the dataset location"""
    client = PipesClient()
    response = client.get_datasets(project_name, project_run_name, model_name, model_run_name)
    if response.status_code == 200:
        datasets = response.json()
        for dataset in datasets:
            if dataset["name"] == dataset_name:
                print_response(f"The location of this dataset is {dataset['location']}")
                return
        print_response(f"Dataset {dataset_name} not found")
    else:
        print_response(f"Encountered error: {response}")


@dataset.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=True,
    help="The project name"
)
@click.option(
    "-r", "--project-run-name",
    type=click.STRING,
    required=True,
    help="The project run name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model name"
)
@click.option(
    "-x", "--modelrun-name",
    type=click.STRING,
    required=True,
    help="The modelrun name"
)
@click.option(
    "-d", "--dataset-name",
    type=click.STRING,
    required=True,
    help="The dataset name"
)
def owner(project_name, projectrun_name, model_name, modelrun_name, dataset_name):
    """Get the dataset owner"""
    client = PipesClient()
    response = client.get_datasets(project_name, projectrun_name, model_name, modelrun_name)
    if response.status_code == 200:
        datasets = response.json()
        for dataset in datasets:
            if dataset["name"] == dataset_name:
                print_response(f"The owner of this dataset is {dataset["registration_author"]}")
                return
        print_response(f"Dataset {dataset_name} not found")
    else:
        print_response(f"Encountered error: {response}")
