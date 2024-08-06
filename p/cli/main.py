"""Console script for pipes."""
import click
from .config import config
from .project import project
from .pipeline import pipeline
from .model import model
from .dataset import dataset
from .service import service
from .task import task
from .login import login
# from pipes.cli.service import service, login

@click.group()
def main(args=None):
    """PIPES CLI client"""

main.add_command(config)
main.add_command(dataset)
main.add_command(task)
main.add_command(login)
main.add_command(project)
main.add_command(pipeline)
main.add_command(model)
main.add_command(service)
main.add_command(login)

if __name__ == "__main__":
    main()
