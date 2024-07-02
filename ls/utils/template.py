import pathlib
import re
import shutil
import sys

import toml

from pipes_cmd.utils.response import print_response


TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "templates"

TEMPLATE_FILES = {
    "project": TEMPLATE_DIR / "project.toml",
    "model": TEMPLATE_DIR / "model.toml",
    "dataset": TEMPLATE_DIR / "dataset.toml",
    "task_planning": {
        "QAQC": TEMPLATE_DIR / "task_planning_qaqc.toml",
        "Transformation": TEMPLATE_DIR / "task_planning_transformation.toml",
        "Visualization": TEMPLATE_DIR / "task_planning_visualization.toml"
    },
    "task_creation": {
        "QAQC": TEMPLATE_DIR / "task_creation_qaqc.toml",
        "Transformation": TEMPLATE_DIR / "task_creation_transformation.toml",
        "Visualization": TEMPLATE_DIR / "task_creation_visualization.toml"
    }
}


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
