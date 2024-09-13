import json
import os
import re
import sys

import click
from requests.models import Response
from requests.exceptions import JSONDecodeError


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


def print_response(response, suppressed=False):
    """
    Print data to stdout console

    Parameters
    ----------
    response: Any
    """
    if isinstance(response, Response):
        if response.status_code < 400:
            if not suppressed:
                print(json.dumps(response.json(), indent=2))
        else:
            try:
                print("Failure: Reason: " + json.dumps(response.json()))
            except JSONDecodeError:
                print("Failure: Reason: " + response.text)
            sys.exit(1)
        return

    if isinstance(response, (dict, list)):
        print(json.dumps(response, indent=2))
        return

    print(response)
