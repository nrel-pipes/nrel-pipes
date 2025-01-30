import json
import sys
import toml
from abc import ABC
from typing import Optional

import requests
from requests.exceptions import ConnectionError

from pipes.auth import get_access_token
from pipes.config import ClientConfig
from pipes.session import Session


class PipesClientBase:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @property
    def token(self):
        return Session().data.get('token', None)

    @property
    def host(self):
        config = ClientConfig()
        host = str(config.pipes_server)
        if host.endswith("/"):
            return host
        return host + "/"

    def ping(self):
        try:
            response = self.get("/api/ping")
        except ConnectionError as e:
            print("Connection Error: Could not connecto to PIPES server. " + str(e))
            sys.exit(1)

        if response.status_code == 200:
            return self.host + " pong"
        else:
            return "Failed to ping " + self.host

    def get(self, url, params=None):
        url = self.host + url
        if params:
            try:
                return requests.get(url, params=params, headers=self.headers)
            except ConnectionError as e:
                print("Connection Error: Could not connecto to PIPES server. " + str(e))
                sys.exit(1)
        else:
            try:
                return requests.get(url, headers=self.headers)
            except ConnectionError as e:
                print("Connection Error: Could not connecto to PIPES server. " + str(e))
                sys.exit(1)

    def post(self, url, data: dict):
        url = self.host + url
        try:
            return requests.post(url, data=json.dumps(data), headers=self.headers)
        except ConnectionError as e:
            print("Connection Error: Could not connecto to PIPES server. " + str(e))
            sys.exit(1)

    def put(self, url, data: dict):
        url = self.host + url
        try:
            return requests.put(url, data=json.dumps(data), headers=self.headers)
        except ConnectionError as e:
            print("Connection Error: Could not connecto to PIPES server. " + str(e))
            sys.exit(1)

    def patch(self, url, data: dict):
        url = self.host + url
        try:
            return requests.patch(url, data=json.dumps(data), headers=self.headers)
        except ConnectionError as e:
            print("Connection Error: Could not connecto to PIPES server. " + str(e))
            sys.exit(1)
