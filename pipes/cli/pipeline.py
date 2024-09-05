import click

from pipes.utils import print_response


@click.group()
def pipeline(args=None):
    """pipeline operation commands"""
