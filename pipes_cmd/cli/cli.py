"""Console script for pipes."""
import click

from pipes_cmd.cli.config import config
from pipes_cmd.cli.project import project
from pipes_cmd.cli.pipeline import pipeline
from pipes_cmd.cli.model import model
from pipes_cmd.cli.dataset import dataset
from pipes_cmd.cli.task import task
from pipes_cmd.cli.service import service, login

@click.group()
def main(args=None):
    """PIPES CLI client"""


main.add_command(config)
main.add_command(dataset)
main.add_command(task)
main.add_command(login)
main.add_command(project)
# main.add_command(pipeline)
main.add_command(model)
main.add_command(service)
