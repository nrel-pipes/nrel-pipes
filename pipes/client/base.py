import json
import os
import toml
from abc import ABC
from typing import Optional

import requests

from pipes.auth import get_access_token
from pipes.config import ClientConfig
from pipes.session import Session


class PipesClientBase:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @property
    def token(self):
        return Session().data.get('token', None)

    @property
    def host(self):
        config = ClientConfig()
        host = str(config.pipes_server)
        if host.endswith("/"):
            return host
        return host + "/"

    def get(self, url, params=None):
        url = self.host + url
        if params:
            response = requests.get(url, params=params, headers=self.headers)
        else:
            response = requests.get(url, headers=self.headers)
        return response

    def post(self, url, data: dict):
        url = self.host + url
        return requests.post(url, data=json.dumps(data), headers=self.headers)

    def ping(self):
        response = self.get("/api/ping")
        if response.status_code == 200:
            return self.host + " pong"
        else:
            return "Failed to ping " + self.host


class PipesClientBase1(ABC):
    def __init__(
            self,
            url: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            token: Optional[str] = None,
            project: Optional[str] = None,
            projectrun: Optional[str] = None,
            model: Optional[str] = None,
            modelrun: Optional[str] = None,
            datasets: Optional[str] = None,
            teams: Optional[str] = None
            ):
        """
        Object is to establish pipes connection with API.
        Logic: 1) get token, 2) declares URL of the API server
        """
        self.url = url if url else None
        self.token = token if token else None
        if not self.token and isinstance(username, str) and isinstance(password, str):
            self.token = get_access_token(username, password)
        else:
            self.pipes_login = False
        self.project = project
        self.projectrun = projectrun
        self.model = model
        self.modelrun = modelrun
        self.datasets = datasets
        self.teams = teams

    def validate(self, ctx):
        """This method validates the client ensuring that it has a valid token and URL."""
        token = get_access_token()
        if not token or not validate_access_token(token) or not validate_access_token(self.token):
            print("You have not properly logged in or token has expired. You must now input your credentials.")
            print(validate_access_token(token))
            self.token = get_access_token()
            self.pipes_login = True
        if self.url is None:
            print("You have not provided a URL. You must now configure your server.")
            self.pipes_login = True
            settings = ClientConfig()
            self.url = settings.get_server()
            print("Re-obtained pipes server")
        return self

    def read_toml(self, file):
        with open(file, "r") as template:
            data = toml.load(template)
        return data

    def get(self, extension, **queries):
        """
        Does get requests for our given api and
        url to get
        """
        url = self.url
        if len(queries) > 0:
            url = f"{url}{extension}/?"
        for query in queries:
            url = f"{url}{query}={queries[query]}{'&' if query != list(queries.keys())[-1] else ''}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=url, headers=headers)
        return response

    def post_toml(self, file, extension, **queries):
        data = self.read_toml(file)
        url = self.url
        if len(queries) > 0:
            url = f"{url}{extension}/?"
        for query in queries:
            url = f"{url}{query}={queries[query]}{'&' if query != list(queries.keys())[-1] else ''}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, json=data, headers=headers)
        return response

    def post_data(self, data, extension, **queries):
        url = self.url + extension
        if queries:
            if "queries" in queries:
                queries = queries["queries"]
            query_str = "&".join([f"{key}={value}" for key, value in queries.items()])
            url = f"{url}?{query_str}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, json=data, headers=headers)
        return response

    def put_data(self, data, extension, **queries):
        url = self.url + extension
        if len(queries) > 1:
            query_str = "&".join([f"{key}={value}" for key, value in queries.items()])
            url = f"{url}?{query_str}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url=url, json=data, headers=headers)
        return response

    def put_team_on_project(self, project, team, data):
        url = f"{self.url}api/teams/detail"
        queries = {
            "project": project,
            "team": team
        }
        if queries:
            query_str = "&".join([f"{key}={value}" for key, value in queries.items()])
            url = f"{url}?{query_str}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url=url, json=data, headers=headers)
        return response

    def check_connection(self):
        response = self.get("", **{})
        if response.status_code == 200:
            return response
        return {"message": "Connection failed"}





    def get_project(self, project=None):
        self.project = project
        return self.get("api/projects", **{"project": project})

    def post_project(self, data):
        if not data:
            raise ValueError("Please provide name of input file")
        # Creating Project
        create_project = data["create_project"]
        project_name = create_project["name"] + "uasdfsxcddasdnw"  # Do not let this line go to production
        create_project["name"] = project_name
        create_project_response = self.post_data(data=create_project, extension="api/projects", queries={})
        if create_project_response.status_code == 201:
            print(f"Project {project_name} created successfully!")
        else:
            raise Exception("Invalid Project configuration.")

        # Put team
        modeling_team = data["create_model"]["modeling_team"]
        modeling_team_data = {
            "name": modeling_team,
            "description": f"Modeling team {modeling_team} for project {project_name}",
            # "members": team["members"]  # Assuming team members are the same
        }
        modeling_team_response = self.post_data(data=modeling_team_data, extension="api/teams", queries={"project": project_name})
        if modeling_team_response.status_code == 201:
            print(f"Modeling team {modeling_team} created successfully!")
        else:
            print(f"Error creating modeling team: {modeling_team_response.json()}")
            raise Exception("Invalid Modeling team configuration.")

        # # Creating projectrun
        create_projectrun = data["create_projectrun"]
        # create_projectrun["project"] = project_name
        projectrun_response = self.post_data(data=create_projectrun, extension="api/projectruns", queries={"project": project_name})
        if projectrun_response.status_code == 201:
            print(f"Project run {create_projectrun['name']} created successfully!")
        else:
            raise Exception("Invalid Project run configuration.")

        # Creating a model
        # breakpoint()
        create_model = data["create_model"]
        create_model["project"] = project_name
        create_model["projectrun"] = create_projectrun["name"]
        model_response = self.post_model_data(data=create_model)
        if model_response.status_code == 201:
            print(f"Model {create_model['name']} created successfully!")
        else:
            print(f"Error creating model: {model_response.json()}")
            raise Exception("Invalid Model configuration.")


    def post_model_data(self, data):
        """
        Method to post model data to the API.
        """
        url = f"{self.url}api/models/?project={data['project']}&projectrun={data['projectrun']}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, json=data, headers=headers)
        # Log response details for debugging
        if response.status_code != 201:
            print(f"Response Content: {response.content}")
        return response

    def get_projectruns(self, project=None):
        if project is not None:
            self.project = project
        if not project:
            raise ValueError("Please provide a project")
        return self.get("api/projectruns", **{"project": self.project})

    def post_projectrun(self, file, project=None):
        if project is not None:
            self.project = project
        if not self.project:
            raise ValueError("Please provide a project and projectrun")
        response = self.post_toml(file, "api/projectruns", project=self.project)
        return response

    def get_models(self, project=None, projectrun=None):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if not project or not projectrun:
            raise ValueError("Please provide a project and projectrun")
        return self.get("api/models", **{"project": project, "projectrun": projectrun})

    def post_model(self, file, project=None, projectrun=None):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if not project or not projectrun:
            raise ValueError("Please provide a project and projectrun")
        return self.post_toml(file, "api/models", project=project, projectrun=projectrun)

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

    def get_datasets(self, project=None, projectrun=None, model=None, modelrun=None):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if model is not None:
            self.model = model
        if modelrun is not None:
            self.modelrun = modelrun
        if not project or not projectrun or not model or not modelrun:
            raise ValueError("Please provide a project, projectrun, model, and modelrun")
        return self.get("api/datasets", **{"project": project, "projectrun": projectrun, "model": model, "modelrun": modelrun})

    def checkin_dataset(self, file, project, projectrun, model, modelrun, adhoc: bool=False):
        if project is not None:
            self.project = project
        if projectrun is not None:
            self.projectrun = projectrun
        if model is not None:
            self.model = model
        if modelrun is not None:
            self.modelrun = modelrun
        if not project or not projectrun or not model or not modelrun:
            raise ValueError("Please provide a project, projectrun, model, and modelrun")
        if adhoc:
            queries = {"project": project, "projectrun": projectrun, "model": model}
        else:
            queries = {"project": project, "projectrun": projectrun, "model": model, "modelrun": modelrun}
        return self.post_toml(file, "api/datasets", **queries)

    def get_teams(self, project=None):
        if project is not None:
            self.project = project
        if not project:
            raise ValueError("Please provide a project")
        return self.get("api/teams", **{"project": project})

    def get_users(self):
        return self.get("api/users")

    def post_user(self, **data):
        return self.post_data(data, "api/users")

    def model_progress(model_context):
        return {"message": "Feature in development"}
