import sys

from requests.exceptions import JSONDecodeError

from .base import PipesClientBase
from pipes.utils import print_response


class ProjectClient(PipesClientBase):

    def list_projects(self):
        return self.get("api/projects/basics")

    def get_project(self, project_name):
        return self.get("api/projects", params={"project": project_name})

    def create_project(self, project_data):
        """Creating a new project includes several different API calls"""
        # Raw data
        try:
            raw_project = project_data["project"]
            raw_projectruns = project_data["project_runs"]
            raw_teams = project_data["model_teams"]
        except KeyError:
            return {
                "detail": "Invalid project data, please check"
            }

        # Project
        p_name = raw_project["name"]
        clean_project = dict(
            name=p_name,
            title=raw_project["full_name"],
            description=raw_project["description"],
            assumptions=raw_project["assumptions"],
            requirements=raw_project["requirements"],
            scenarios=raw_project["scenarios"],
            sensitivities=raw_project["sensitivities"],
            milestones=raw_project["milestones"],
            scheduled_start=raw_project["scheduled_start"],
            scheduled_end=raw_project["scheduled_end"],
            owner=raw_project["owner"],
        )

        p_url = f"api/projects"
        print_response(f"Creating project '{p_name}' from template...")
        response = self.post(p_url, data=clean_project)
        print_response(response, suppressed=True)

        # Teams
        t_url = f"api/teams?project={p_name}"
        for team in raw_teams:
            t_name = team["name"]
            print_response(f"Creating team '{t_name}'...")
            response = self.post(t_url, data=team)
            print_response(response, suppressed=True)

        # Project runs
        pr_url = f"api/projectruns?project={p_name}"
        for projectrun in raw_projectruns:
            pr_name = projectrun["name"]
            print_response(f"Creating project run '{pr_name}'...")
            response = self.post(pr_url, data=projectrun)
            print_response(response, suppressed=True)

            # Add models to project runs
            m_url = f"api/models?project={p_name}&projectrun={pr_name}"
            print(m_url)
            for raw_model in projectrun["models"]:
                clean_model = raw_model.copy()
                clean_model["name"] = raw_model["model"]
                m_name = clean_model["name"]
                print_response(f"Creating model '{m_name}' under project run '{pr_name}'")
                if not clean_model.get("modeling_team", None):
                    clean_model["modeling_team"] = raw_model["model"]
                response = self.post(m_url, data=clean_model)
                print_response(response, suppressed=True)

            # Create handoff plans
            topology = projectrun["topology"]
            handoffs = []
            for topo in topology:
                for h in topo["handoffs"]:
                    clean_handoff = {
                        "from_model": topo["from_model"],
                        "to_model": topo["to_model"],
                        "name": h["id"],
                        "description": h["description"],
                        "scheduled_start": h["scheduled_start"],
                        "scheduled_end": h["scheduled_end"],
                        "notes": h["notes"],
                    }
                    handoffs.append(clean_handoff)
            h_url = f"api/handoffs?project={p_name}&projectrun={pr_name}"
            print_response(f"Creating handoffs under project run '{pr_name}'...")
            response = self.post(h_url, data=handoffs)
            print_response(response, suppressed=True)

        return {
            "detail": f"Project '{p_name}' created successfully."
        }
