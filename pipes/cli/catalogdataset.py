import click
import os
import sys
import json

from pipes.cli.login import login
from pipes.auth import validate_session_token
from pipes.session import Session

from pipes.template import load_template, copy_template
from pipes.client import PipesClient
from pipes.utils import print_response, prompt_overwrite


@click.group()
@click.pass_context
def catalogdataset(ctx):
    """Catalog dataset operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@catalogdataset.command()
def list():
    """List all available datasets"""
    client = PipesClient()
    response = client.list_catalogdatasets()
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@catalogdataset.command()
@click.option(
    "-d", "--dataset-name",
    type=str,
    required=False,
    help="The dataset name must be unique"
)
@click.option(
    "--owner",
    is_flag=True,
    help="Filter dataset owner"
)
def get(dataset_name, owner):
    """Get given dataset metadata"""
    session = Session()

    dataset = None
    if session.contains("dataset"):
        _dataset = session.get("dataset")
        if _dataset["name"] == dataset_name:
            dataset = _dataset

    if not dataset:
        client = PipesClient()
        response = client.get_catalogdataset(dataset_name=dataset_name)

        if response.status_code >= 500:
            print_response(response.text)
            return

        if response.status_code == 200:
            dataset = response.json()
            session.update({"dataset": dataset})
        else:
            print_response(response.json())
            return

    if owner:
        print_response(dataset["owner"])
        return

    print_response(dataset)


@catalogdataset.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The dataset template file"
)
def create(template_file):
    """Create dataset from template"""
    data = load_template(template_file)
    client = PipesClient()
    response = client.create_catalogdataset(data)
    if 'detail' in response.json():
        print_response(response.json()['detail'])
    else:
        print_response(response.json())

@catalogdataset.command()
@click.option(
    "-d", "--dataset-name",
    type=str,
    required=False,
    help="The dataset name must match an existing dataset for update"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=False,
    help="The dataset template file. For updates, the template may include a subset of fields to update."
)
@click.option(
    "-u", "--update-data",
    type=str,
    required=False,
    help="The dataset data to update in JSON format. This option can be used as an alternative to the template file for quick updates. For example: '{\"name\": \"Updated dataset name\"}'"
)
def update(dataset_name, template_file, update_data):
    """Update dataset from template or JSON data"""
    if template_file and update_data:
        print("Please provide either a template file or update data, not both.")
        return
    elif template_file:
        data = load_template(template_file)
    elif update_data:
        try:
            data = json.loads(update_data)
        except json.JSONDecodeError:
            print("Invalid JSON format for update data.")
            return
    else:
        print("Please provide either a template file or update data for the update.")
        return
    client = PipesClient()
    response = client.update_catalogdataset(dataset_name, data)
    if 'detail' in response.json():
        print_response(response.json()['detail'])
    else:
        print_response(response.json())

@catalogdataset.command()
@click.option(
    "-o", "--output-file",
    type=click.Path(),
    default=None,
    help="Output template path",
    callback=prompt_overwrite
)
def template(output_file):
    """Get project related template"""
    if not output_file:
        output_file = "catalogdataset.toml"

    copy_to_dir = os.path.dirname(output_file)
    if copy_to_dir and not os.path.exists(copy_to_dir):
        os.makedirs(copy_to_dir, exist_ok=True)

    copy_template('catalogdataset', output_file)

    print(f"Template generated: {output_file}")
