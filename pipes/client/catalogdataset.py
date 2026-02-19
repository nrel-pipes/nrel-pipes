import sys, json

import requests
from requests.exceptions import JSONDecodeError

from .base import PipesClientBase
from pipes.utils import print_response


class CatalogDatasetClient(PipesClientBase):

    def list_catalogdatasets(self):
        return self.get("api/catalogdatasets")

    def get_catalogdataset(self, dataset_name):
        return self.get(f"api/catalogdataset/detail?dataset_name={dataset_name}")

    def create_catalogdataset(self, dataset_data):
        return self.post("api/catalogdataset/create", data=dataset_data)
    
    def update_catalogdataset(self, dataset_name, dataset_data):
        return self.patch("api/catalogdataset/update", params={"dataset_name": dataset_name}, data=dataset_data)

        