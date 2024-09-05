import json
import os
import re

import click


def validate_email_input(value):
    regex = re.compile(r"^[A-Za-z0-9]+([._%+-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+$")
    if not re.fullmatch(regex, value):
        print("Not a valid email address.")
        return None
    return value


def prompt_overwrite(ctx, param, value):
    """Callback to prompt the user to confirm if the CLI should overwrite the
    file."""

    if os.path.exists(str(value)):
        click.confirm(f"File exists at '{value}'. Overwrite?", abort=True)

    return value


def print_response(data):
    """
    Print data to stdout console

    Parameters
    ----------
    data : dict
    """
    if not data or not isinstance(data, (dict, list)):
        print(data)
    else:
        print(json.dumps(data, indent=2))
