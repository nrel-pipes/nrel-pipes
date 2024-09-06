
from .base import PipesClientBase


class TeamClient(PipesClientBase):

    def create_team(self, project_name, team_data):
        return self.post(f"api/teams?project={project_name}", data=team_data)

    def list_teams(self, project_name):
        return self.get("api/teams", params={"project": project_name})

    def get_team(self, project_name, team_name):
        response = self.get("api/teams", params={"project": project_name})
        if response and response.status_code == 200:
            for team in response.json():
                if team["name"] == team_name:
                    return team
        return None

    def update_team(self, project_name, team_name, team_data):
        print(team_data)
        return self.put(f"api/teams/detail?project={project_name}&team={team_name}", data=team_data)
