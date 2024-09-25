from .base import PipesClientBase


class ProjectRunClient(PipesClientBase):

    def list_projectruns(self, project_name):
        return self.get("api/projectruns", params={"project": project_name})

    def create_projectruns(self, project_name, projectruns_data):
        pr_url = f"api/projectruns?project={project_name}"

        if isinstance(projectruns_data, dict):
            projectruns_data = [projectruns_data]

        for projectrun in projectruns_data:
            self.post(pr_url, data=projectrun)

        return {
            "detail": "Project runs created successfully"
        }
