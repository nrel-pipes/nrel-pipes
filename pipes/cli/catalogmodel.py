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
def catalogmodel(ctx):
    """Catalog model operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@catalogmodel.command()
def list():
    """List all available models"""
    client = PipesClient()
    response = client.list_catalogmodels()
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@catalogmodel.command()
@click.option(
    "-m", "--model-name",
    type=str,
    required=False,
    help="The model name must be unique"
)
@click.option(
    "--owner",
    is_flag=True,
    help="Filter model owner"
)
def get(model_name, owner):
    """Get given model metadata"""
    session = Session()

    model = None
    if session.contains("model"):
        _model = session.get("model")
        if _model["name"] == model_name:
            model = _model

    if not model:
        client = PipesClient()
        response = client.get_catalogmodel(model_name=model_name)

        if response.status_code >= 500:
            print_response(response.text)
            return

        if response.status_code == 200:
            model = response.json()
            session.update({"model": model})
        else:
            print_response(response.json())
            return

    if owner:
        print_response(model["owner"])
        return

    print_response(model)


@catalogmodel.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The model template file"
)
def create(template_file):
    """Create model from template"""
    data = load_template(template_file)
    client = PipesClient()
    response = client.create_catalogmodel(data)
    print_response(response["detail"])

@catalogmodel.command()
@click.option(
    "-m", "--model-name",
    type=str,
    required=False,
    help="The model name must match an existing model for update"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=False,
    help="The model template file. For updates, the template may include a subset of fields to update."
)
@click.option(
    "-u", "--update-data",
    type=str,
    required=False,
    help="The model data to update in JSON format. This option can be used as an alternative to the template file for quick updates. For example: '{\"name\": \"Updated model name\"}'"
)
def update(model_name, template_file, update_data):
    """Update model from template or JSON data"""
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
    response = client.update_catalogmodel(model_name, data)
    if 'detail' in response.json():
        print_response(response.json()['detail'])
    else:
        print_response(response.json())

# @catalogmodel.command()
# @click.option(
#     "-t", "--type-name",
#     type=click.Choice([
#         'model-creation',
#     ]),
#     required=True,
#     help="Choose a template type"
# )
# @click.option(
#     "-o", "--output-file",
#     type=click.Path(),
#     default=None,
#     help="Output template path",
#     callback=prompt_overwrite
# )
# def template(type_name, output_file):
#     """Get project related template"""
#     if not output_file:
#         output_file = type_name + ".toml"

#     _, ext = os.path.splitext(output_file)
#     if not ext or "toml" not in ext.lower():
#         print("Only .toml file is support as output")
#         sys.exit(1)

#     copy_to_dir = os.path.dirname(output_file)
#     if copy_to_dir and not os.path.exists(copy_to_dir):
#         os.makedirs(copy_to_dir, exist_ok=True)

#     copy_template(type_name, output_file)

#     print(f"Template generated: {output_file}")
