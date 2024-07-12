from abc import ABC, abstractmethod
import os
import toml
from typing import Optional
from dotenv import load_dotenv
# from auth import get_cognito_access_token
import requests
from .base import PipesClientBase
load_dotenv()


class ModelRunClient(ABC):
    def get_modelruns(self, project, projectrun, model):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if model is not None: 
            self.model = model
        if not project or not projectrun or not model:
            raise ValueError("Please provide a project, projectrun, and model")
        return self.get("api/modelruns", **{"project": project, "projectrun": projectrun, "model": model})
    
    def post_modelrun(self, file, project=None, projectrun=None, model=None):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if model is not None:
            self.model = model
        if not project or not projectrun or not model:
            raise ValueError("Please provide a project, projectrun, and model")
        return self.post_toml(file, "api/modelruns", project=project, projectrun=projectrun, model=model)
