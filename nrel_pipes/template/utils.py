import pathlib
import re
import shutil
import sys

import toml

from nrel_pipes.utils import print_response
from nrel_pipes.template import TEMPLATE_FILES


def copy_template(typename, filename, subtype=None):
    """Get the PIPES template TOML file"""
    if typename not in TEMPLATE_FILES:
        raise ValueError("Invalid template type, supprted types: {}", TEMPLATE_FILES.keys())

    template = TEMPLATE_FILES[typename]
    if subtype:
        template = template[subtype]
    shutil.copyfile(src=template, dst=filename)


def load_template(filename):
    """Load data from .toml file"""
    with open(filename) as f:
        try:
            data = toml.load(f)
        except Exception as error:
            response = {
                "code": "N/A",
                "details": f"Failed to load template '{filename}'. {type(error).__name__}: {error}."
            }
            print_response(response)
            sys.exit(1)

    return data


def dump_template(data, filename):
    """Dump data to .toml file"""
    with open(filename, "w") as f:
        try:
            toml.dump(data, f)
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
