from .base import PipesClientBase

class ModelClient(PipesClientBase):

    def list_models(self, project_name, projectrun_name=None):
        params = {"project": project_name}
        if projectrun_name:
            params["projectrun_name"] = projectrun_name
        return self.get("api/models", params=params)

    def create_model(self, project_name, projectrun_name, models_data):
        m_url = f"api/models?project={project_name}&projectrun={projectrun_name}"
        return self.post(m_url, data=models_data)

    def check_model_progress(self, project_name, projectrun_name, model_name):
        return {"detail": "This feature is in development."}
