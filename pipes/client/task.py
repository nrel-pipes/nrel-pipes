from .base import PipesClientBase

class TaskClient(PipesClientBase):

    def update_task(self, task_status):
        requests.patch()
