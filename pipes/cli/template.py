import os
import sys

import click

from pipes.template import copy_template
from pipes.utils import prompt_overwrite


@click.group()
def template(args=None):
    """Template operation commands"""



@template.command()
@click.option(
    "-t", "--type-name",
    type=click.Choice([
        'project-creation',
        'team-creation'
    ]),
    required=True,
    help="Choose the type of template"
)
@click.option(
    "-o", "--output-file",
    type=click.Path(),
    default=None,
    help="Output template path",
    callback=prompt_overwrite
)
def get(type_name, output_file):
    """Get a toml template"""
    if not output_file:
        output_file = type_name + ".toml"

    _, ext = os.path.splitext(output_file)
    if not ext or "toml" not in ext.lower():
        print("Only .toml file is support as output")
        sys.exit(1)

    copy_to_dir = os.path.dirname(output_file)
    if copy_to_dir and not os.path.exists(copy_to_dir):
        os.makedirs(copy_to_dir, exist_ok=True)

    copy_template(typename=type_name, filename=output_file)

    print(f"Template created at {output_file}")



# @dataset.command()
# @click.option(
#     "-s", "--system",
#     type=click.Choice(SYSTEM_TYPES, case_sensitive=True),
#     required=True,
#     help="""Choose a system from the following: ["ESIFRepoAPI", "AmazonS3", "HPCStorage", "DataFoundry"]"""
# )
# @click.option(
#     "-o", "--output",
#     type=click.Path(),
#     default="dataset-template.toml",
#     callback=prompt_overwrite,
#     help="The filename of output template"
# )
# def get_checkin_template(system, output):
#     """Get a copy of dataset checkin template in toml"""
#     _, ext = os.path.splitext(output)
#     if not ext or "toml" not in ext.lower():
#         response = {
#             "code": "INVALID_ARGUMENT",
#             "details": "Only .toml file is support as output"
#         }
#         print_response(response)
#         sys.exit(1)
#     dataset_schema = load_template(TEMPLATE_FILES["dataset"])
#     dataset_schema["dataset"]["type"] = covert_camel_to_snake(system)
#     dump_template(dataset_schema, output)

#     print_response(f"Output toml at location {output}")
