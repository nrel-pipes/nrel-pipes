import os
import sys
import toml
from pprint import pprint
import click
from p.utils import print_response, dump_template, load_template, TEMPLATE_FILES, covert_camel_to_snake, prompt_overwrite, get_token, ClientSettings
from typing import Optional
from p.client import DatasetClient
from p.cli.login import login

SYSTEM_TYPES = ["ESIFRepoAPI", "AmazonS3", "HPCStorage", "DataFoundry"]
settings = ClientSettings()

dataset = {
    "name": "s5",
    "display_name": "string",
    "description": "",
    "version": "string",
    "hash_value": "",
    "version_status": "Active",
    "previous_version": "string",
    "data_format": "string",
    "schema_info": "",
    "weather_years": [],
    "model_years": [],
    "units": [],
    "scenarios": [
        "string"
    ],
    "sensitivities": [],
    "relevant_links": [],
    "comments": "",
    "resource_url": "",
    "location": {},
    "registration_author": {
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "organization": "string"
    },
    "temporal_info": {},
    "spatial_info": {},
    "source_code": {
        "location": "string",
        "branch": "",
        "tag": "",
        "image": ""
    },
    "other": {}
}




@click.group()
def dataset(args=None):
    """dataset operation commands"""


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
    help="The model name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.pass_context
def list_datasets(ctx, project_name, project_run_name, model_name, model_run_name):
    """List all datasets under a model run"""
    client = DatasetClient(url=settings.get_server(), token=get_token())
    client.validate(ctx)
    response = client.get_datasets(project_name, project_run_name, model_name, model_run_name)
    if response.status_code == 200:
        print_response(response.json())
    else:
        print_response(f"Encountered error: {response}")

@dataset.command()
@click.option(
    "--dataset",
    type=click.STRING,
    required=True,
    help="The dataset name"
)
def checkout_dataset(dataset):
    """Checkout project dataset"""
    response = {
        "code": "N/A",
        "details": "Feature not implemented yet"
    }
    print_response(response)


@dataset.command()
@click.option(
    "-s", "--system",
    type=click.Choice(SYSTEM_TYPES, case_sensitive=True),
    required=True,
    help="""Choose a system from the following: ["ESIFRepoAPI", "AmazonS3", "HPCStorage", "DataFoundry"]"""
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default="dataset-template.toml",
    callback=prompt_overwrite,
    help="The filename of output template"
)
def get_checkin_template(system, output):
    """Get a copy of dataset checkin template in toml"""
    _, ext = os.path.splitext(output)
    if not ext or "toml" not in ext.lower():
        response = {
            "code": "INVALID_ARGUMENT",
            "details": "Only .toml file is support as output"
        }
        print_response(response)
        sys.exit(1)
    dataset_schema = load_template(TEMPLATE_FILES["dataset"])
    dataset_schema["dataset"]["type"] = covert_camel_to_snake(system)
    dump_template(dataset_schema, output)

    print_response(f"Output toml at location {output}")


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
@click.pass_context
def checkin_dataset(ctx, project_name, project_run_name, model_name, model_run_name, template_file, metadata_validation, adhoc):
    """Check-in project dataset"""
    client = DatasetClient(url=settings.get_server(), token=get_token())
    client.validate(ctx)
    response = client.checkin_dataset(template_file, project_name, project_run_name, model_name, model_run_name, adhoc)
    if response.status_code == 201:
        print_response("Dataset successfully checked in.")
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
@click.pass_context
def get_dataset_owner(ctx, project_name, project_run_name, model_name, model_run_name, dataset_name):
    """Get dataset owner"""
    client = DatasetClient(url=settings.get_server(), token=get_token())
    client.validate(ctx)
    response = client.get_datasets(project_name, project_run_name, model_name, model_run_name)
    if response.status_code == 200:
        datasets = response.json()
        for dataset in datasets:
            if dataset["name"] == dataset_name:
                print_response(f"The owner of this dataset is {dataset["registration_author"]}")
                return
        print_response(f"Dataset {dataset_name} not found")
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
@click.pass_context
def get_dataset_location(ctx, project_name, project_run_name, model_name, model_run_name, dataset_name):
    """Get dataset location"""
    client = DatasetClient(url=settings.get_server(), token=get_token())
    client.validate(ctx)
    response = client.get_datasets(project_name, project_run_name, model_name, model_run_name)
    if response.status_code == 200:
        datasets = response.json()
        for dataset in datasets:
            if dataset["name"] == dataset_name:
                print_response(f"The location of this dataset is {dataset["location"]}")
                return
        print_response(f"Dataset {dataset_name} not found")
    else:
        print_response(f"Encountered error: {response}")
