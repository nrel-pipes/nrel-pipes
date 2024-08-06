import json
import click
import requests
import toml
from p.utils import prompt_overwrite, get_selected_user_context_from_session, print_response, load_template, ClientSettings, get_or_create_pipes_session, get_token
from p.client import ModelClient


settings = ClientSettings()
TOKEN = get_token()

@click.group()
def model(args=None):
    """model operation commands"""


@model.command()
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The project template path"
)
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
def create_model(template_file, project_name, project_run_name):
    """pipes model create-model -f example_data/model/create_model.toml -p test1 -r 1"""
    with open(template_file, "r") as template:
        model = toml.load(template)
    settings = ClientSettings()
    session = get_or_create_pipes_session()
    response = requests.post(
        url = f"{settings.pipes_server}api/models/?project={project_name}&projectrun={project_run_name}",
        json = model,
        headers = {
            "Authorization": f"Bearer {session.data["token"]}",
        }
    )
    if response.status_code == 201:
        print_response(f"Model created successfully for {template_file}.")
    else:
        print_response(f"Error in creating model: \n{response.json()}")


@model.command()
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
@click.pass_context
def list_models(ctx, project_name, project_run_name):
    """List all models under a project run"""
    client = ModelClient(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.get_models(project_name, project_run_name)
    if response.status_code == 200:
        print_response(response.json())
    else:
        print_response(f"Encountered error: {response}")


@model.command()
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
    help="The project run name"
)
@click.option(
    "-f", "--template-file",
    type=click.Path(exists=True),
    required=True,
    help="The model run template path"
)
@click.pass_context
def create_model_run(ctx, project_name, project_run_name, model_name, template_file):
    """Create model run under given model"""
    client = ModelClient(url=settings.get_server(), token=TOKEN)  
    client.validate(ctx)
    response = client.post_modelrun(template_file, project_name, project_run_name, model_name)
    if response.status_code == 201:
        print_response(f"Model run has successfully posted.")
    else:
        print_response(f"Model run failed to post with error {response.json()}")


@model.command()
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
    "-o", "--output",
    type=click.Path(),
    default="model_run_template.toml",
    required=True,
    help="Filepath to save model run template to.",
    is_eager=True,
    callback=prompt_overwrite
)
@click.pass_context
def get_model_run_template(ctx, project_name, project_run_name, model_name, output):
    """Get model run template for input model"""
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

    project_name = context_data["project_name"]
    project_run_name = context_data["project_run_name"]
    client = ModelClient(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.get_model_run_template_data(project_name, project_run_name, model_name)
    data = response.get("handoff_data", {"handoffs": {}})
    if not data["handoffs"]:
        print("Warning: model run template does not contain handoffs")

    client.generate_model_run_template(data, output)


@model.command()
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
@click.pass_context
def check_model_run_progress(ctx, project_name, project_run_name, model_name, model_run_name):
    """Check the model run prcogress"""
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
    client = ModelClient(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.check_model_run_progress(context_data)
    print_response(response)


@model.command()
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
@click.pass_context
def close_model_run(ctx, project_name, project_run_name, model_name, model_run_name):
    """Close specified model run"""
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
    client = ModelClient(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.close_model_run(context_data)
    print_response(response)


@model.command()
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
@click.pass_context
def check_model_progress(ctx, project_name, project_run_name, model_name):
    """Check the model progress"""
    model_context = {
        "project_name": project_name,
        "project_run_name": project_run_name,
        "model_name": model_name
    }
    client = ModelClient(url=settings.get_server(), token=TOKEN)
    client.validate(ctx)
    response = client.check_model_progress(model_context)
    print_response(response)
