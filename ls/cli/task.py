import json
import os
import sys

import click

from pipes_cmd.utils.cli import prompt_overwrite, get_selected_user_context_from_session
from pipes_cmd.utils.response import print_response
from pipes_cmd.utils.template import copy_template, load_template


@click.group()
def task(args=None):
    """task operation commands"""


@task.command()
@click.option(
    "-t", "--task-type",
    type=click.Choice(["Transformation", "QAQC", "Visualization"], case_sensitive=True),
    default=None,
    help="The task type"
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default="task-planning-template.toml",
    help="The template output path",
    callback=prompt_overwrite
)
def get_task_planning_template(task_type, output):
    """Get task planning template"""
    _, ext = os.path.splitext(output)
    if not ext or "toml" not in ext.lower():
        response = {
            "code": "INVALID_ARGUMENT",
            "details": "Only .toml file is support as output"
        }
        print_response(response)
        sys.exit(1)

    copy_template(typename="task_planning", filename=output, subtype=task_type)
    print_response({"output": output})



@task.command()
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
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-i", "--task-id",
    type=click.STRING,
    required=True,
    help="The task id"
)
def get_task(project_name, project_run_name, model_name, model_run_name, task_id):
    """Get task by using id under given handoff"""
    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
    })

    response = client.get_task(context_data, task_id)
    print_response(response)


@task.command()
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
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-h", "--handoff-id",
    type=click.STRING,
    required=False,
    help="The handoff id"
)
@click.option(
    "-t", "--task-type",
    type=click.Choice(["Transformation", "QAQC", "Visualization"], case_sensitive=False),
    default=None,
    help="The task type"
)
def list_tasks(project_name, project_run_name, model_name, model_run_name, handoff_id, task_type):
    """List tasks using under handoff"""
    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
    })

    response = client.list_tasks(context_data, handoff_id, task_type)
    print_response(response)


@task.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=True,
    help="The project name"
)
@click.option(
    "-r", "--project-run-name",
    type=click.STRING,
    required=True,
    help="The project run name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The task template path"
)
def plan_tasks(project_name, project_run_name, model_name, model_run_name, template_file):
    """Plan adhoc tasks using given template"""
    template_data = load_template(template_file)
    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
    })

    response = client.plan_tasks(context_data, template_data)
    print_response(response)


@task.command()
@click.option(
    "-t", "--task-type",
    type=click.Choice(["Transformation", "QAQC", "Visualization"], case_sensitive=True),
    default=None,
    help="The task type"
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default="task-creation-template.toml",
    help="The template output path",
    callback=prompt_overwrite
)
def get_task_creation_template(task_type, output):
    """Get task creation template"""
    _, ext = os.path.splitext(output)
    if not ext or "toml" not in ext.lower():
        response = {
            "code": "INVALID_ARGUMENT",
            "details": "Only .toml file is support as output"
        }
        print_response(response)
        sys.exit(1)

    copy_template(typename="task_creation", filename=output, subtype=task_type)
    print_response({"output": output})


@task.command()
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
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-f", "--task-file",
    type=click.Path(exists=True),
    required=True,
    help="The task creation toml filepath"
)
@click.option(
    "-d", "--dataset-file",
    type=click.Path(exists=True),
    required=False,
    help="Filepath for transformed dataset (if applicable)"
)
@click.option(
    "--task-pass/--task-fail",
    is_flag=True,
    default=None,
    required=True,
    help="Set task status for this creation."
)
def create_tasks(project_name, project_run_name, model_name, model_run_name, task_file, dataset_file, task_pass):
    """Create a set of tasks in a task creation toml."""
    
    if task_pass:
        task_status = "PASS"
    else:
        task_status = "FAIL"

    task_data = load_template(task_file)

    if dataset_file:
        dataset_data = load_template(dataset_file)

    else:
        dataset_data = {}

    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
    })

    response = client.create_tasks(context_data, task_data, dataset_data, task_status)
    print_response(response)


@task.command()
@click.option(
    "-p", "--project-name",
    type=click.STRING,
    required=True,
    help="The project name"
)
@click.option(
    "-r", "--project-run-name",
    type=click.STRING,
    required=True,
    help="The project run name"
)
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-t", "--task-name",
    type=click.STRING,
    required=True,
    help="The task name"
)
def get_task_status(project_name, project_run_name, model_name, model_run_name, task_name):
    """Get the task status on given task"""
    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
        "task_name": task_name
    })

    response = client.get_task_status(context_data)
    print_response(response)


@task.command()
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
@click.option(
    "-m", "--model-name",
    type=click.STRING,
    required=True,
    help="The model name"
)
@click.option(
    "-x", "--model-run-name",
    type=click.STRING,
    required=True,
    help="The model run name"
)
@click.option(
    "-t", "--task-name",
    type=click.STRING,
    required=True,
    help="The task name"
)
@click.option(
    "--task-pass/--task-fail",
    is_flag=True,
    default=None,
    help="Set task status for this task."
)
def update_task_status(project_name, project_run_name, model_name, model_run_name, task_name, task_pass):
    """Update the task status on given task"""
    if task_pass is None:
        print("The flag option --task-pass or --task-fail is required, please specify it in command.")
        sys.exit(1)

    if task_pass:
        task_status = "PASS"
    else:
        task_status = "FAIL"

    if project_name and project_run_name:
        context_data = {
            "project_name": project_name,
            "project_run_name": project_run_name,
        }
    else:
        selected = get_selected_user_context_from_session()
        context_data = {
            "project_name": selected["project"]["data"]["name"],
            "project_run_name": selected["project_run"]["data"]["name"]
        }
        print("Use info from session: ", json.dumps(context_data))

    context_data.update({
        "model_name": model_name,
        "model_run_name": model_run_name,
        "task_name": task_name
    })

    response = client.update_task_status(context_data, task_status)
    print_response(response)
