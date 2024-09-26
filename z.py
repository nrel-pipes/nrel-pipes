import os
from dotenv import load_dotenv
from pipes.auth import initiate_auth
from pipes.sdk import PIPES

load_dotenv()

project = "lambda_project"
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
              'project': 'lambda_project',
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

pipes = PIPES()
# pipes.token = "eyJraWQiOiJ1eVF6YSszNjdcL205N3ZDTCtFeGZpQkFOeEJhZ1hyUTQyR1pCZUxwVHRGVT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwMzY0MTFiNi01NWQyLTQxMDEtYmE0MS0yYTQ3NzAwMWY4ZDkiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9SekVMMkNPT3EiLCJjbGllbnRfaWQiOiJjbGZwbGkxYXZ0NmVpbDAzb3ZyMTFxZHBpIiwib3JpZ2luX2p0aSI6ImJjN2FhZGMwLWY5YzYtNDQwYi05YTZjLTRiNmFjNTI0ZjIxMyIsImV2ZW50X2lkIjoiNTcyYjdiYjMtODNmMS00ZmYwLWJlNTUtMTQ1YTM5OTY4ZjFiIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcyNzM2Mzc0MCwiZXhwIjoxNzI3NDUwMTQwLCJpYXQiOjE3MjczNjM3NDAsImp0aSI6IjIyMGQzZGUxLTVjMmUtNGUxMC04MzI5LTQzZDZhZjBhNzViOSIsInVzZXJuYW1lIjoiMDM2NDExYjYtNTVkMi00MTAxLWJhNDEtMmE0NzcwMDFmOGQ5In0.InPMHXScjbbGQBca8eImdycP2CcSTWXwpsIJd3GxO1CuqnRaSkZz7BzeCM3KvNkpRplV3E6d4eLZnc3XChN_zdgB53_Z8Kew9zVOMiCcIgwkTRrIEI6KJWpbJG92B0WnhT0RwGwUFVNkPHecykPUwkkDBir-w6oqje_H65WvmXazV1J_BvaipYWXqiGFdcWWHTPM4gzudIrxEXseAsqAIBbuh4ZfbZTk4AHtgZM--DX6GdjA0JERmZyOYGdH5aB_rmkfSG3PrFIzJ1bPHiBcNP6N_GhcvLxSBsEN2f2sdZtOMvER1FLI10aPsWtP6HuzcT-fzPfMle5swTjNo2te6w"
# pipes.create_pipes_task("lambda_project", "lambda_project_run", "lambda_model", "lambda_model_run", task)

if __name__=="__main__":
  pipes = PIPES()
  print(pipes.create_pipes_task("lambda_project", "lambda_project_run", "lambda_model", "lambda_model_run", task))
  # print(pipes.get_pipes_project("testTask2"))
  # print(pipes.get_modelruns(project, project_run, model))
  # print(pipes.get_tasks(project, project_run, model, model_run))
  # print(pipes.create_pipes_task(project, project_run, model, model_run, sample_task))
  # print(pipes.update_task(project, project_run, model, model_run, task, status))
  # print(pipes.add_task("name", {"Stuff": "Stuff"}))
  # queue = pipes.read_hero_task()
  # print(len(queue))
  # print(pipes.read_hero_queue())
  # print(pipes.pull_hero_task())  
  # queue = pipes.read_hero_task()
  # print(len(queue))
