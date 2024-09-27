import os
from dotenv import load_dotenv
from pipes.auth import initiate_auth
from pipes.sdk import PIPES

load_dotenv()

project = "lambda_project2"
project_run = "lambda_project_run"
model = "lambda_model"
model_run = "lambda_model_run"
task = "sample_task4"
status = "SUCCESS"

task = {'assignee': {'email': 'Jordan.Eisenman@nrel.gov',
               'first_name': 'Jordan',
               'last_name': 'Eisenman',
               'organization': 'nrel'},
  'completion_date': '2023-12-20T23:59:59.997Z',
  'context': {'model': 'lambda_model',
              'modelrun': 'lambda_model_run',
              'project': 'lambda_project2',
              'projectrun': 'lambda_project_run'},
  'description': '',
  'input_datasets': [],
  'input_parameters': {},
  'logs': '',
  'name': 'lambda_task_a2dd345d3dsdffdfd2f45',
  'notes': '',
  'output_datasets': [],
  'output_values': {},
  'scheduled_end': '2023-12-30T23:59:59.997Z',
  'scheduled_start': '2023-01-02T00:00:00.005Z',
  'source_code': {'branch': '', 'image': '', 'location': 'string', 'tag': ''},
  'status': 'PENDING',
  'subtasks': [{'description': '', 'name': 'string'}],
  'type': 'string'}
import os
from hero import HeroClient, get_env_variable
import json
from dotenv import load_dotenv


load_dotenv()

try:
    HERO_QUEUE_ID = os.environ.get("HERO_QUEUE_ID")
    HERO_ENV = os.environ.get('HERO_ENV', 'dev')
    HERO_PROJECT = os.environ.get('HERO_PROJECT')
except EnvironmentError as e:
    print(e)
    exit(1)

APPLICATION_ID = f'{HERO_ENV}-{HERO_PROJECT}'

pipes = PIPES()

if __name__=="__main__":
  pipes = PIPES()
  print(pipes.get_pipes_tasks("lambda_project2", "lambda_project_run", "lambda_model", "lambda_model_run"))
  # print(pipes.create_pipes_task("lambda_project", "lambda_project_run", "lambda_model", "lambda_model_run", task))
  # print(pipes.get_pipes_project("testTask2"))
  # print(pipes.get_modelruns(project, project_run, model))
  # print(pipes.get_tasks(project, project_run, model, model_run))
  # print(pipes.create_pipes_task(project, project_run, model, model_run, sample_task))
  # print(pipes.update_task(project, project_run, model, model_run, task, status))
  # hero_task = pipes.add_hero_task("name", metadata={"Stuff": "Stuffs"})
  # hero_task_id = hero_task["id"]
  # print("Hero Task ID ", hero_task_id)
  # print(pipes.pull_hero_task_metadata(hero_task_id))
  # print(hero_task)
  # print(hero_task)
  pipes.get_pipes_task("lambda_project2", "lambda_project_run", "lambda_model", "lambda_model_run", "lambda_task_edfdedwf")