from .base import PipesClientBase

class ProjectRunClient(PipesClientBase):
    def get_projectruns(self, project=None):
        if project is not None:
            self.project = project
        if not project:
            raise ValueError("Please provide a project")
        return self.get("api/projectruns", **{"project": self.project})

    def post_projectrun(self, file, project=None):
        if project is not None:
            self.project = project
        if not self.project:
            raise ValueError("Please provide a project and projectrun")
        response = self.post_toml(file, "api/projectruns", project=self.project)
        return response
