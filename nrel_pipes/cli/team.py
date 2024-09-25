import click
import os
import sys

from nrel_pipes.cli.login import login
from nrel_pipes.auth import validate_session_token
from nrel_pipes.client import PipesClient
from nrel_pipes.template import load_template, copy_template, dump_template
from nrel_pipes.utils import print_response, prompt_overwrite


@click.group()
@click.pass_context
def team(ctx):
    """Project operation commands"""
    if not validate_session_token():
        print("PIPES session expired or invalid, please login")
        ctx.invoke(login)


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="project short name"
)
def list(project_name):
    """List all teams under given project"""
    client = PipesClient()
    response = client.list_teams(project_name=project_name)
    if response.status_code >= 500:
        print_response(response.text)
        return
    print_response(response.json())


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="project short name"
)
@click.option(
    "-t", "--team-name",
    type=str,
    required=True,
    help="team name"
)
def get(project_name, team_name):
    """Get one project team"""
    client = PipesClient()
    team = client.get_team(project_name, team_name)
    if not team:
        print(f"No team named '{team_name}' under project '{project_name}'")
        return
    print_response(team)


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="The project template path"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create(project_name, template_file):
    """Create new project team"""
    team_data = load_template(template_file)

    client = PipesClient()
    response = client.create_team(project_name, team_data)
    if response.status_code >= 500:
        print_response(response.text)
        return

    print_response(response.json())


@team.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="The project template path"
)
@click.option(
    "-t", "--team-name",
    type=str,
    required=True,
    help="team name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=False,
    help="Template file"
)
def update(project_name, team_name, template_file):
    """Update team info and/or members"""
    team_data = load_template(template_file)

    client = PipesClient()
    response = client.update_team(project_name, team_name, team_data)
    if response.status_code >= 500:
        print_response(response.text)
        return

    print_response(response.json())



@team.command()
@click.option(
    "-t", "--type-name",
    type=click.Choice([
        'team-creation',
        'team-update'
    ]),
    required=True,
    help="Choose a template type"
)
@click.option(
    "-p", "--project-name",
    type=str,
    default=None,
    help="The project template path"
)
@click.option(
    "-n", "--team-name",
    type=str,
    default=None,
    help="team name"
)
@click.option(
    "-o", "--output-file",
    type=click.Path(),
    default=None,
    help="Output template path",
    callback=prompt_overwrite
)
def template(type_name, project_name, team_name, output_file):
    """Get team related template"""
    if not output_file:
        output_file = type_name + ".toml"

    _, ext = os.path.splitext(output_file)
    if not ext or "toml" not in ext.lower():
        print("Only .toml file is support as output")
        sys.exit(1)

    copy_to_dir = os.path.dirname(output_file)
    if copy_to_dir and not os.path.exists(copy_to_dir):
        os.makedirs(copy_to_dir, exist_ok=True)

    success = False

    # Generate template based on type
    if type_name == "team-creation":
        copy_template(type_name, output_file)
        success = True

    if type_name == "team-update":
        if not project_name:
            print("Option '-p/--project-name' is required for getting team update template.")
            return

        if not team_name:
            print("Option '-n/--team-name' is required for getting team update template.")
            return

        client = PipesClient()
        result = client.get_team(project_name=project_name, team_name=team_name)
        if not result:
            print_response("Failed to generate template." )
        else:
            dump_template(result, output_file)
            success = True

    if success:
        print(f"Template generated: {output_file}")
