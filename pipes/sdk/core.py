import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import requests
import boto3
import json
from .auth import get_pipes_token, get_hero_token, valid_cognito_token
from .task_engine import HeroTaskEngine
from pipes.client import TaskClient

load_dotenv()
SCOPES = ["task-engine/user"]
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
PIPES_SQS_URL = os.getenv("PIPES_SQS_URL")
AWS_REGION = os.getenv("AWS_REGION")

class PIPES(ABC):
    def __init__(
            self,
            task_engine_id=os.getenv("HERO_DATA_HUB_PROJECT"), 
            project="pipes_hero", 
            project_run="pipes_hero_prun", 
            model="dsgrid",
            model_run="pipes_hero"
        ):
        """
        Constructor for PIPES class
        """
        # --------------- Pipes ---------------#
        # Pipes Auth
        self.cognito_client_id = os.getenv('PIPES_COGNITO_CLIENT_ID')
        self.pipes_token = get_pipes_token(os.getenv('USERNAME'), os.getenv('PASSWORD'))
        self.url = os.getenv('PIPES_URL', "http://localhost:8080/")
        self.client_key = os.getenv('PIPES_CLIENT_KEY')
        # Pipes Queue
        self.pipes_sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION  # Specify your AWS region
        )

        self.pipes_queue_url = PIPES_SQS_URL
        # Pipes Task
        self.project = project
        self.project_run = project_run
        self.model = model
        self.model_run = model_run
        self.pipes_task_client = TaskClient(url=self.url, token=self.pipes_token, project=project, projectrun=project_run, model=model, modelrun=model_run)

        # --------------- Hero --------------- #
        # Hero Project Configurations
        self.hero_project = os.getenv('HERO_PROJECT')
        self.client_id = os.getenv('HERO_CLIENT_ID')
        self.client_secret = os.getenv('HERO_CLIENT_SECRET')
        self.data_hub_project = os.getenv('HERO_DATA_HUB_PROJECT')
        self.data_repo_api_url = os.getenv('HERO_DATA_REPO_API_URL')
        self.queue_id = os.getenv('HERO_QUEUE_ID')
        self.cognito_api_url = os.getenv('HERO_COGNITO_API_URL')
        self.task_engine_api_url = os.getenv('HERO_TASK_ENGINE_API_URL')
        self.task_engine = HeroTaskEngine(task_engine_id)
        self.hero_token = get_hero_token(client_id=self.client_id, client_secret=self.client_secret, scopes=SCOPES)

    def validate_pipes_token(self):
        """This method validates the client ensuring that it has a valid token and URL."""
        if not self.pipes_token or not valid_cognito_token(self.pipes_token):
            print("You have not properly logged in or token has expired. You must now input your credentials.")
            print(valid_cognito_token(self.pipes_token))
            self.pipes_login = True
            print("You have not properly logged in")
        if self.url is None:
            print("You have not provided a URL. You must now configure your server.")
        if not (not self.pipes_token or not valid_cognito_token(self.pipes_token)) and self.url:
            return True
        return False

    def validate_hero_token(self):
        return valid_cognito_token(self.hero_token)
    
    def push_hero_task(self, task):
        hte = self.task_engine.push_task(task)
        return hte
    
    def post_pipes_task(self, task, status="PENDING"):
        print(self.pipes_task_client.post_task(task, status))

    def update_pipes_task_status(self, task, status):
        print(self.pipes_task_client.patch_task(task, status=status))
