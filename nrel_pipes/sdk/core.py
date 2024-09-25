import os
import json
import requests
from hero import HeroClient, get_env_variable
from dotenv import load_dotenv
from nrel_pipes.client import PipesClient, ProjectClient, ModelRunClient, TaskClient
from nrel_pipes.auth import get_access_token
from nrel_pipes.auth import initiate_auth

load_dotenv()

class PIPES(object):
    def __init__(self):
        if os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("AWS_LAMBDA_RUNTIME_API") and not os.environ.get("TOKEN"):
            self.token = initiate_auth(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))
        elif os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("AWS_LAMBDA_RUNTIME_API"):
            self.token = os.environ.get("TOKEN")
        else:
            self.token = get_access_token()
        self.host = os.environ.get("PIPES_URL")
        self.hero_env = get_env_variable('HERO_ENV', 'dev')
        self.hero_project = get_env_variable('HERO_PROJECT', "nrel-kg")
        self.application_id = f'{self.hero_env}-{self.hero_project}'
        self.hero_queue_id= os.environ.get("HERO_QUEUE_ID")
        self.hero = HeroClient()
        self.hero.authenticate()
        self.task_engine = self.hero.TaskEngine(self.application_id)

    def get_pipes_pipes_project(self, project):
        project_client = ProjectClient()
        return project_client.get_project(project).json()
    
    def get_pipes_modelruns(self, project_name, projectrun_name, model_name):
        model_client = ModelRunClient()
        return model_client.list_modelruns(project_name, projectrun_name, model_name).json()

    def get_pipes_tasks(self, project_name, projectrun_name, model_name, modelrun_name):
        print("Pulling task from PIPES...")
        task_client = TaskClient()
        return task_client.get_tasks(project_name, projectrun_name, model_name, modelrun_name).json()

    def create_pipes_task(self, project_name, projectrun_name, model_name, modelrun_name, task_data):
        task_client = TaskClient()
        return task_client.create_task(project_name, projectrun_name, model_name, modelrun_name, task_data)

    def update_pipes_task(self, project_name, projectrun_name, model_name, modelrun_name, task, status):
        task_client = TaskClient()
        return task_client.update_task(project_name, projectrun_name, model_name, modelrun_name, task, status).json()

    def add_hero_task(self, name, metatype='Task', metadata={}):
        return self.task_engine.add_task(self.hero_queue_id, name, metatype, metadata)

    def read_hero_task(self):
        return self.task_engine.read_tasks(self.hero_queue_id)[0]

    def pull_hero_task(self):
        task_id = self.task_engine.read_tasks(self.hero_queue_id)[0]['id']
        return self.task_engine.delete_task(task_id)

    def read_hero_queue(self):
        return self.task_engine.read_queue(self.hero_queue_id)
