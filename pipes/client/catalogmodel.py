import sys

from requests.exceptions import JSONDecodeError

from .base import PipesClientBase
from pipes.utils import print_response


class CatalogModelClient(PipesClientBase):

    def list_catalogmodels(self):
        return self.get("api/catalogmodels")

    def get_catalogmodel(self, model_name):
        return self.get(f"api/catalogmodel/detail?model_name={model_name}")

    def create_catalogmodel(self, model_data):
        # Check for schema and schema_version in the model data
        if "catalog_schema" not in model_data or "schema_version" not in model_data:
            return {
                "detail": "Invalid model data, please ensure both 'catalog_schema' and 'schema_version' are included."
            }

        return self.post("api/catalogmodel/create", data=model_data)

    def update_catalogmodel(self, model_name, model_data):
        return self.patch("api/catalogmodel/update", params={"model_name": model_name}, data=model_data)
