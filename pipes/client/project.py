from .base import PipesClientBase

class ProjectClient(PipesClientBase):
    def get_project(self, project=None):
        self.project = project
        return self.get("api/projects", **{"project": project})

    def post_project(self, data):
        if not data:
            raise ValueError("Please provide name of input file")
        # Creating Project
        create_project = data["create_project"]
        project_name = create_project["name"] + "uasdfsxcddasdnw"  # Do not let this line go to production
        create_project["name"] = project_name
        create_project_response = self.post_data(data=create_project, extension="api/projects", queries={})
        if create_project_response.status_code == 201:
            print(f"Project {project_name} created successfully!")
        else:
            raise Exception("Invalid Project configuration.")
        
        # Put team
        modeling_team = data["create_model"]["modeling_team"]
        modeling_team_data = {
            "name": modeling_team,
            "description": f"Modeling team {modeling_team} for project {project_name}",
            # "members": team["members"]  # Assuming team members are the same
        }
        modeling_team_response = self.post_data(data=modeling_team_data, extension="api/teams", queries={"project": project_name})
        if modeling_team_response.status_code == 201:
            print(f"Modeling team {modeling_team} created successfully!")
        else:
            print(f"Error creating modeling team: {modeling_team_response.json()}")
            raise Exception("Invalid Modeling team configuration.")
        
        # # Creating projectrun
        create_projectrun = data["create_projectrun"]
        # create_projectrun["project"] = project_name
        projectrun_response = self.post_data(data=create_projectrun, extension="api/projectruns", queries={"project": project_name})
        if projectrun_response.status_code == 201:
            print(f"Project run {create_projectrun['name']} created successfully!")
        else:
            raise Exception("Invalid Project run configuration.")
        
        # Creating a model
        # breakpoint()
        create_model = data["create_model"]
        create_model["project"] = project_name
        create_model["projectrun"] = create_projectrun["name"]
        model_response = self.post_model_data(data=create_model)
        if model_response.status_code == 201:
            print(f"Model {create_model['name']} created successfully!")
        else:
            print(f"Error creating model: {model_response.json()}")
            raise Exception("Invalid Model configuration.")
        
