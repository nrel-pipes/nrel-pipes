
from .project import ProjectClient
from .projectrun import ProjectRunClient
from .model import ModelClient
from .modelrun import ModelRunClient
from .dataset import DatasetClient
from .team import TeamClient
from .task import TaskClient
from .user import UserClient


class PipesClient(
    ProjectClient,
    ProjectRunClient,
    ModelClient,
    ModelRunClient,
    DatasetClient,
    TeamClient,
    UserClient,
):
    pass
