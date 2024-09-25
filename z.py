import os
from dotenv import load_dotenv
from nrel_pipes.auth import initiate_auth
from nrel_pipes.sdk import PIPES

load_dotenv()

project = "lambda_project"
project_run = "lambda_project_run"
model = "lambda_model"
model_run = "lambda_model_run"
task = "sample_task3"
status = "SUCCESS"

sample_task = {
  "name": "sample_task3",
  "type": "string",
  "description": "",
  "assignee": {
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "organization": "string"
  },
  "status": "PENDING",
  "subtasks": [
    {
      "name": "string",
      "description": ""
    }
  ],
  "scheduled_start": "2024-09-19T20:29:38.589Z",
  "scheduled_end": "2024-09-19T20:29:38.589Z",
  "completion_date": "2024-09-19T20:29:38.589Z",
  "source_code": {
    "location": "string",
    "branch": "",
    "tag": "",
    "image": ""
  },
  "input_datasets": [],
  "input_parameters": {},
  "output_datasets": [],
  "output_values": {},
  "logs": "",
  "notes": ""
}



if __name__=="__main__":
  pipes = PIPES()
  # print(pipes.get_pipes_project("testTask2"))
  # print(pipes.get_modelruns(project, project_run, model))
  # print(pipes.get_tasks(project, project_run, model, model_run))
  # print(pipes.create_task(project, project_run, model, model_run, sample_task))
  # print(pipes.update_task(project, project_run, model, model_run, task, status))
  # print(pipes.add_task("name", {"Stuff": "Stuff"}))
  # queue = pipes.read_hero_task()
  # print(len(queue))
  # print(pipes.read_hero_queue())
  print(pipes.pull_hero_task())  
  # queue = pipes.read_hero_task()
  # print(len(queue))
