from .base import PipesClientBase

class TaskClient(PipesClientBase):
    def post_task(self, task, status="PENDING"):
        self.post_data(task, extension="api/tasks", queries={
            "project": self.project, 
            "projectrun": self.projectrun, 
            "model": self.model,
            "modelrun": self.modelrun,
            "status": status
            })

    def get_tasks(self, project=None, projectrun=None, model=None, modelrun=None):
        pass
    
    def patch_task(self, task_name, status="PENDING"):
        self.patch_data(extension="api/tasks", queries={
            "project": self.project, 
            "projectrun": self.projectrun, 
            "model": self.model,
            "modelrun": self.modelrun,
            "task": task_name,
            "status": status
        })
