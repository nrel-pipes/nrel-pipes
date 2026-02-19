import pathlib
import re
import shutil
import sys

import toml
import yaml
import json

from pipes.utils import print_response
from pipes.template import TEMPLATE_FILES


def copy_template(typename, filename, subtype=None):
    """Get the PIPES template TOML file"""
    if typename not in TEMPLATE_FILES:
        raise ValueError("Invalid template type, supprted types: {}", TEMPLATE_FILES.keys())

    template = TEMPLATE_FILES[typename]
    if subtype:
        template = template[subtype]
    shutil.copyfile(src=template, dst=filename)


def load_template(filename):
    """Load data from supported file types (TOML/YAML/JSON)"""
    with open(filename) as f:
        if filename.endswith(".toml"):
            try:
                data = toml.load(f)
            except Exception as error:
                response = {
                    "code": "N/A",
                    "details": f"Failed to load TOML template '{filename}'. {type(error).__name__}: {error}."
                }
                print_response(response)
                sys.exit(1)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as error:
                response = {
                    "code": "N/A",
                    "details": f"Failed to load YAML template '{filename}'. {type(error).__name__}: {error}."
                }
                print_response(response)
                sys.exit(1)
        elif filename.endswith(".json"):
            try:
                data = json.load(f)
            except json.JSONDecodeError as error:
                response = {
                    "code": "N/A",
                    "details": f"Failed to load JSON template '{filename}'. {type(error).__name__}: {error}."
                }
                print_response(response)
                sys.exit(1)
        else:
            print_response({
                "code": "N/A",
                "details": f"Unsupported template file type for '{filename}'. Supported types are: .toml, .yaml/.yml, .json."
            })
            sys.exit(1)

    return data


def dump_template(data, filename):
    """Dump data to .toml/.yaml/.json file"""
    with open(filename, "w") as f:
        try:
            if filename.endswith(".toml"):
                toml.dump(data, f)
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                yaml.safe_dump(data, f)
            elif filename.endswith(".json"):
                json.dump(data, f)
        except Exception as error:
            response = {
                "code": "N/A",
                "details": f"Failed to dump template '{filename}'. {type(error).__name__}: {error}."
            }
            print_response(response)
            sys.exit(1)


def covert_camel_to_snake(value):
    """Convert camel case to snake case."""
    value = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", value).lower()
