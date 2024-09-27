import os
from typing import Dict, List, Optional, Any

import requests
from hero import HeroClient
from dotenv import load_dotenv
from pipes.client import PipesClient, ProjectClient, ModelRunClient, TaskClient
from pipes.auth import get_access_token
from pipes.auth import initiate_auth

load_dotenv()

class PIPES(object):
    """
    If local: 
        - Use use code to grab token from .pipes session
    """
    def __init__(self):
        """
        This will be re-factored, don't you fret!
        """
        if os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("AWS_LAMBDA_RUNTIME_API") and not os.environ.get("TOKEN"):
            username, password, client_id = os.environ.get("USERNAME"), os.environ.get("PASSWORD"), os.environ.get("PIPES_COGNITO_CLIENT_ID")
            self.token = initiate_auth(username, password, aws=True)
        elif os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("AWS_LAMBDA_RUNTIME_API"):
            self.token = os.environ.get("TOKEN")
        else:
            self.token = get_access_token()
        self.host = os.environ.get("PIPES_URL")
        self.hero_env = os.environ.get('HERO_ENV', 'dev')
        self.hero_project = os.environ.get('HERO_PROJECT')
        self.application_id = f'{self.hero_env}-{self.hero_project}'
        self.hero_queue_id= os.environ.get("HERO_QUEUE_ID")
        self.hero = HeroClient()
        self.hero.authenticate()
        print(self.hero_queue_id)
        self.task_engine = self.hero.TaskEngine(self.application_id)

    def get_pipes_pipes_project(self, project: str) -> requests.Response:
        project_client = ProjectClient()
        return project_client.get_project(project)
    
    def get_pipes_modelruns(self, project_name: str, projectrun_name: str, model_name: str) -> requests.Response:
        model_client = ModelRunClient()
        return model_client.list_modelruns(project_name, projectrun_name, model_name)

    def get_pipes_tasks(self, project_name: str, projectrun_name: str, model_name: str, modelrun_name: str) -> requests.Response:
        print("Pulling task from PIPES...")
        task_client = TaskClient()
        return task_client.get_tasks(project_name, projectrun_name, model_name, modelrun_name)

    def create_pipes_task(self, project_name: str, projectrun_name: str, model_name: str, modelrun_name: str, task_data: str) -> requests.Response:
        task_client = TaskClient()
        return task_client.create_task(project_name, projectrun_name, model_name, modelrun_name, task_data)

    def update_pipes_task(self, project_name: str, projectrun_name: str, model_name: str, modelrun_name: str, task: str, status: str) -> requests.Response:
        task_client = TaskClient()
        return task_client.update_task(project_name, projectrun_name, model_name, modelrun_name, task, status)
    
    def get_pipes_task(self, project_name: str, projectrun_name: str, model_name: str, modelrun_name: str, task: str) -> requests.Response:
        task_client = TaskClient()
        return task_client.get_tasks(project_name, projectrun_name, model_name, modelrun_name, task)

    def add_hero_task(self, name: str, metatype: str = 'Task', metadata: Dict[str, Any] = {}) -> Dict[str, Any]:
        return self.task_engine.add_task(queue_id=self.hero_queue_id, name=name, metatype=metatype, metadata=metadata)

    def read_hero_task(self, task_id: str) -> Dict[str, Any]:
        return self.task_engine.read_task(self.hero_queue_id, task_id)

    def pull_hero_task(self, task_id: str) -> Dict[str, Any]:
        hero_task = self.task_engine.read_task(task_id)
        task_id = hero_task['id']
        self.task_engine.delete_task(task_id)
        return hero_task 

    def pull_hero_task_metadata(self, task_id: str) -> Dict[str, Any]:
        hero_task = self.task_engine.read_task(task_id)
        task_id = hero_task['id']
        self.task_engine.delete_task(task_id)
        task_meta_data = hero_task.get("metadata", {})
        return task_meta_data 

    def read_hero_queue(self) -> Dict[str, Any]:
        return self.task_engine.read_queue(self.hero_queue_id)
