from .base import PipesClientBase

class TaskClient(PipesClientBase):
    def get_tasks(self, project=None, projectrun=None, model=None, modelrun=None):
        return self.get("api/tasks", params={"project": project, "projectrun": projectrun, "model": model, "modelrun": modelrun})

    def create_task(self, project, projectrun, model, modelrun, task_data):
        url = "api/tasks"
        params = {
            "project": project,
            "projectrun": projectrun,
            "model": model,
            "modelrun": modelrun
        }
        return self.post(url, data=task_data, params=params)

    def update_task(self, project, projectrun, model, modelrun, task_name, status):
        url = "api/tasks"
        params = {
            "project": project,
            "projectrun": projectrun,
            "model": model,
            "modelrun": modelrun,
            "task": task_name,
            "status": status
        }
        response = self.patch(url, params=params)
        return response
