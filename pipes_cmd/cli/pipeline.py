import click

from pipes_cmd.utils.response import print_response


@click.group()
def pipeline(args=None):
    """pipeline operation commands"""


@pipeline.command()
@click.option(
    "--project",
    type=click.STRING,
    required=True,
    help="The project name"
)
def list(project):
    """Show pipeline information"""
    response = {
        "code": "N/A",
        "details": "Feature not implemented yet"
    }
    print_response(response)


@pipeline.command()
@click.option(
    "--pipeline",
    type=click.STRING,
    required=True,
    help="The pipeline name"
)
def show_schedule(pipeline):
    """Show the schedule of given pipeline"""
    response = {
        "code": "N/A",
        "details": "Feature not implemented yet"
    }
    print_response(response)
