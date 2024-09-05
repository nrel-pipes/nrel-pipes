"""Console script for pipes."""
import click

from .config import config
from .login import login
from .project import project
from .projectrun import projectrun
from .model import model
from .modelrun import modelrun
from .dataset import dataset
from .server import server
from .task import task
from .team import team
from .template import template
from .user import user




@click.group()
def main(args=None):
    """PIPES CLI client"""


main.add_command(config)
main.add_command(login)
main.add_command(template)
main.add_command(server)

main.add_command(project)
main.add_command(projectrun)
main.add_command(model)
main.add_command(modelrun)
main.add_command(dataset)
main.add_command(task)

main.add_command(team)
main.add_command(user)



if __name__ == "__main__":
    main()
