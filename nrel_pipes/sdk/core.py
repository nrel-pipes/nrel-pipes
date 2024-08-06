import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import requests
import boto3
import json
from .auth import get_pipes_token, get_hero_token, valid_cognito_token
from .task_engine import HeroTaskEngine
from ..client import TaskClient

load_dotenv()
SCOPES = ["task-engine/user"]
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
PIPES_SQS_URL = os.getenv("PIPES_SQS_URL")
AWS_REGION = os.getenv("AWS_REGION")

import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import requests
import boto3
import json
from .auth import get_pipes_token, get_hero_token, valid_cognito_token
from .task_engine import HeroTaskEngine

load_dotenv()
SCOPES = ["task-engine/user"]

class PIPES(ABC):
    def __init__(
            self,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            pipes_sqs_url=os.getenv("PIPES_SQS_URL"),
            aws_region=os.getenv("AWS_REGION"),
            pipes_cognito_client_id=os.getenv('PIPES_COGNITO_CLIENT_ID'),
            username=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD'),
            pipes_url=os.getenv('PIPES_URL', "http://localhost:8080/"),
            pipes_client_key=os.getenv('PIPES_CLIENT_KEY'),
            hero_project=os.getenv('HERO_PROJECT'),
            hero_client_id=os.getenv('HERO_CLIENT_ID'),
            hero_client_secret=os.getenv('HERO_CLIENT_SECRET'),
            hero_data_hub_project=os.getenv('HERO_DATA_HUB_PROJECT'),
            hero_data_repo_api_url=os.getenv('HERO_DATA_REPO_API_URL'),
            hero_queue_id=os.getenv('HERO_QUEUE_ID'),
            hero_cognito_api_url=os.getenv('HERO_COGNITO_API_URL'),
            hero_task_engine_api_url=os.getenv('HERO_TASK_ENGINE_API_URL'),
            task_engine_id=os.getenv("HERO_DATA_HUB_PROJECT"),
            project="pipes_hero", 
            project_run="pipes_hero_prun", 
            model="dsgrid",
            model_run="pipes_hero"
        ):
        """
        Constructor for PIPES class

        Please ensure the following environment variables are set:
        
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_SESSION_TOKEN
        - PIPES_SQS_URL
        - AWS_REGION
        - PIPES_COGNITO_CLIENT_ID
        - USERNAME
        - PASSWORD
        - PIPES_URL (default: "http://localhost:8080/")
        - PIPES_CLIENT_KEY
        - HERO_PROJECT
        - HERO_CLIENT_ID
        - HERO_CLIENT_SECRET
        - HERO_DATA_HUB_PROJECT
        - HERO_DATA_REPO_API_URL
        - HERO_QUEUE_ID
        - HERO_COGNITO_API_URL
        - HERO_TASK_ENGINE_API_URL

        Arguments can also be passed directly to override the environment variables.
        """
        # --------------- Pipes ---------------#
        self.cognito_client_id = pipes_cognito_client_id
        self.pipes_token = get_pipes_token(username, password)
        self.url = pipes_url
        self.client_key = pipes_client_key
        self.pipes_sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=aws_region  # Specify your AWS region
        )
        self.pipes_queue_url = pipes_sqs_url
        self.project = project
        self.project_run = project_run
        self.model = model
        self.model_run = model_run
        self.pipes_task_client = TaskClient(url=self.url, token=self.pipes_token, project=project, projectrun=project_run, model=model, modelrun=model_run)

        # --------------- Hero --------------- #
        self.hero_project = hero_project
        self.client_id = hero_client_id
        self.client_secret = hero_client_secret
        self.data_hub_project = hero_data_hub_project
        self.data_repo_api_url = hero_data_repo_api_url
        self.queue_id = hero_queue_id
        self.cognito_api_url = hero_cognito_api_url
        self.task_engine_api_url = hero_task_engine_api_url
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
        return self.pipes_task_client.patch_task(task, status=status)