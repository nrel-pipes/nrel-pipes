from .base import PipesClientBase

class TaskClient(PipesClientBase):
    def get_tasks(self, project=None, projectrun=None, model=None, modelrun=None):
        return self.get("api/tasks", params={"project": project, "projectrun": projectrun, "model": model, "modelrun": modelrun})
    
    def get_task(self, task_name, project=None, projectrun=None, model=None, modelrun=None):
        tasks = self.get_tasks(project, projectrun, model, modelrun)
        for task in tasks:
            if task['name'] == task_name:
                return task
        return None  # Return None if the task is not found

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
