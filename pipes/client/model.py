from .base import PipesClientBase

class ModelClient(PipesClientBase):
    def check_connection(self):
        response = self.get("", **{})
        if response.status_code == 200:
            return response
        return {"message": "Connection failed"}

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
    
    def model_progress(model_context):
        return {"message": "Feature in development"}
