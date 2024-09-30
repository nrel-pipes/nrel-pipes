from .base import PipesClientBase


class ModelRunClient(PipesClientBase):
    def list_modelruns(self, project_name, projectrun_name, model_name):
        params = {
            "project": project_name,
        }
        if projectrun_name:
            params["projectrun"] = projectrun_name
        if model_name:
            params["model"] = model_name
        return self.get("api/modelruns", params=params)

    def create_modelrun(self, project_name,  projectrun_name, model_name, modelruns_data):
        mr_url = f"api/modelruns?project={project_name}&projectrun={projectrun_name}&model={model_name}"
        return self.post(mr_url, data=modelruns_data)
