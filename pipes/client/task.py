from typing import Optional, Dict, Any, List
from .base import PipesClientBase

class TaskClient(PipesClientBase):
    def get_tasks(self, project=None, projectrun=None, model=None, modelrun=None):
        return self.get("api/tasks", params={"project": project, "projectrun": projectrun, "model": model, "modelrun": modelrun})
    
    def get_task(self, project: str, projectrun: str, model: str, modelrun: str, task_name: str) -> Optional[Dict[str, Any]]:
        response = self.get_tasks(project, projectrun, model, modelrun)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                if task['name'] == task_name:
                    return task
        return None 

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
