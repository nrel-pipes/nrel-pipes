from typing import Optional
from .base import PipesClientBase
from pipes.utils import get_cognito_access_token

class DatasetClient(PipesClientBase):
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
        Object is to establish pipes connection with api.
        Logic: 1) get token, 2) declares URL of the API server
        """
        if token:
            self.token = token
        else:
            self.token = get_cognito_access_token(username, password)
        self.url = url
        self.project = project
        self.projectrun = projectrun
        self.model = model
        self.modelrun = modelrun
        self.datasets = datasets
        self.teams = teams

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

if __name__=="__main__":
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
