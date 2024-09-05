from .base import PipesClientBase


class DatasetClient(PipesClientBase):

    def list_datasets(self, project_name, projectrun_name, model_name, modelrun_name):
        params = {
            "project": project_name,
            "projectrun": projectrun_name,
            "model": model_name,
            "modelrun": modelrun_name
        }
        return self.get("api/datasets", params=params)

    def checkin_dataset(self, project_name, projectrun_name, model_name, modelrun_name, dataset_data, adhoc = False):
        d_url = f"api/datasets?project={project_name}&projectrun={projectrun_name}&model={model_name}&modelrun={modelrun_name}"
        return self.post(d_url, data=dataset_data, adhoc=adhoc)
