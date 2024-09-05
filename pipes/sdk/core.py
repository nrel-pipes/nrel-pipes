import requests

from pipes.client import PipesClient


class PIPES(object):

    def __init__(self):
        pass

    def get_project(self):
        response = requests.get(url, headers)
        return response

    def get_modelrun(self):
        pass

    def get_task(self):
        print("Pulling task from PIPES...")
        pass

    def create_task(self):
        # API call
        # response = requests.post(url, headers)
        return response

    def update_task(self, task, source):
        client = PipesClient()
        client.update_task()
        client.create_dataset()
