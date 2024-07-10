import toml
import os
import sys
import click
import requests
import json
from pipes.utils import (
    get_token, get_or_create_pipes_session, prompt_overwrite,
    get_selected_user_context_from_session, print_response,
    copy_template, load_template, ClientSettings
)
from pipes.client import ProjectClient



settings = ClientSettings()
TOKEN = get_token()
CLIENT = ProjectClient(url=settings.get_server(), token=TOKEN)

@click.group()
def project(args=None):
    """project operation commands"""


@project.command()
@click.option(
    "-o", "--output",
    type=click.Path(),
    default="project-template.toml",
    help="The project output path",
    callback=prompt_overwrite
)
def get_init_template(output):
    """Get project initialization template"""
    _, ext = os.path.splitext(output)
    if not ext or "toml" not in ext.lower():
        response = {
            "code": "INVALID_ARGUMENT",
            "details": "Only .toml file is support as output"
        }
        print_response(response)
        sys.exit(1)

    copy_template(typename="project", filename=output)
    print_response({"output": output})

@project.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
@click.option(
    "-p", "--project",
    type=str,
    required=True,
    help="The project template path"
)
def create_team(template_file, project):
    with open(template_file, "r") as template:
        team = toml.load(template)
    settings = ClientSettings()
    response = requests.post(
        url = f"{settings.pipes_server}api/teams/?project={project}",
        json = team,
        headers = {
            "Authorization": f"Bearer {TOKEN}",
        }
    )
    # response = pipes.create_team(team)
    if response.status_code == 201:
        print_response(f"Team created successfully for {template_file}.")
    else:
        print_response(f"Error in creating team: \n{response.json()}")


@project.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=False,
    help="Template file"
)
@click.option(
    "-t", "--team",
    type=str,
    required=False,
    help="Team name"
)
@click.option(
    "-p", "--project",
    type=str,
    required=True,
    help="The project template path"
)
def put_team_on_project(project, template_file=None, team=None):
    """pipes project put-team-on-project -t dsgrid -p test1 -f """
    settings = ClientSettings()
    session = get_or_create_pipes_session()
    """pipes project put-team-on-project -f example_data/project/put_team.toml -p test1"""
    with open(template_file, "r") as template:
        team = toml.load(template)
    team_name = team["name"]
    response = requests.put(
        url = f"{settings.pipes_server}api/teams/detail/?project={project}&team={team_name}",
        json = team,
        headers = {
            "Authorization": f"Bearer {session.data['token']}",
        }
    )
    print(response.status_code)
    if response.status_code == 200:
        print_response(f"Team added to project successfully for {template_file}.")
    else:
        print_response(f"Error in adding team to project: \n{response.json()}")

@project.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create_project(template_file):
    """Create project based on given template"""
    with open(template_file, "r") as template:
        project = toml.load(template)
    settings = ClientSettings()
    session = get_or_create_pipes_session()
    create_project_response = CLIENT.post_project(project)


@project.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=False,
    help="Name of project"
)
def get_project(project_name):
    """Get project metadata"""
    response = CLIENT.get_project(project_name)
    if response.status_code == 200:
        print_response(response.json())
    else:
        print_response(f"Could not get project. Error message: {response.json()}")

@project.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=False,
    help="Name of project"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def update_project(project_name, template_file):
    """Update project or project run metadata."""
    if project_name:
        context_data = {"project_name": project_name}
    else:
        selected = get_selected_user_context_from_session()
        context_data = {"project_name": selected["project"]["data"]["name"]}
        print("Use info from session: ", json.dumps(context_data))

    template_data = load_template(template_file)

    response = CLIENT.update_project(context_data, template_data)
    print_response(response)


@project.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=True,
    help="Name of project"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
def create_project_run(project_name, template_file):
    """Create a new project run in an existing project."""
    response = CLIENT.post_projectrun(template_file, project_name)
    if response.status_code == 201:
        print(f"Project run successfully created for {project_name}")
    else:
        print(f"Project run failed for {project_name}, status: {response.status_code}")

@project.command()
@click.option(
    "-p", "--project-name",
    type=str,
    required=False,
    help="Name of project"
)
def get_project_owner(project_name):
    """Get the owner of given project"""
    response = CLIENT.get_project(project_name)
    if response.status_code == 200:
        print_response(response.json()["owner"])
    else:
        print_response(f"Could not get project. Error message: {response.json()}")


@project.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=False,
    help="The project name"
)
@click.option(
    "-r", "--project-run-name",
    type=click.STRING,
    required=False,
    help="The project run name"
)
def check_project_run_progress(project_name, project_run_name):
    """Check the project run progress"""
    if project_name and project_run_name:
        project_run_context = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        project_run_context = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(project_run_context))

    response = CLIENT.check_project_run_progress(project_run_context)
    print_response(response)
