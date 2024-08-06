import requests
from dotenv import load_dotenv
import logging
import math
import time
from tenacity import retry_if_exception_type

load_dotenv()

COGNITO_AUTH_URL = "https://dev-nrel-research.auth.us-west-2.amazoncognito.com/oauth2/token"
import urllib3
urllib3.disable_warnings()

class HeroRetryError(RuntimeError):
    def __init__(self, message, attempt_number, idle_for):
        super().__init__(message)
        self.attempt_number = attempt_number
        self.idle_for = idle_for

class ClientPullTasksEmpty(Exception):
    pass

class ApiUnauthorized(Exception):
    pass

class ApiQueueDoesNotExist(Exception):
    pass

class ApiItemNotFound(Exception):
    pass

class ClientQueueNotActive(Exception):
    pass

class ClientReadyTaskEstimate(Exception):
    pass

class ClientRetry(Exception):
    pass

class ClientNoQueueObject(Exception):
    pass

class ClientCreateProject(Exception):
    pass

class ClientCreateDataset(Exception):
    pass

class ClientCreateFileObject(Exception):
    pass

task_engine_exceptions = (
    retry_if_exception_type(ApiUnauthorized)
    | retry_if_exception_type(ApiQueueDoesNotExist)
    | retry_if_exception_type(ApiItemNotFound)
    | retry_if_exception_type(ClientQueueNotActive)
    | retry_if_exception_type(ClientNoQueueObject)
    | retry_if_exception_type(ClientPullTasksEmpty)
    | retry_if_exception_type(ClientReadyTaskEstimate)
    | retry_if_exception_type(ClientRetry)
)

data_repo_exceptions = (
    retry_if_exception_type(ApiUnauthorized)
    | retry_if_exception_type(ApiQueueDoesNotExist)
    | retry_if_exception_type(ClientCreateProject)
    | retry_if_exception_type(ClientCreateDataset)
    | retry_if_exception_type(ClientCreateFileObject)
)

class ResilientSession(requests.Session):
    def request(self, method, url, **kwargs):
        counter = 0
        max_retries = 10
        while counter < max_retries:
            counter += 1
            r = super(ResilientSession, self).request(method, url, **kwargs)
            if r.status_code in [429, 456, 500, 502, 503, 504, 569, 563]:
                print(r.status_code, r.json().get("error"))
                delay = (5 * math.pow(2, counter)) * 0.5
                logging.warning(
                    "Got recoverable error [%s]: retry #%s in %ss from %s %s, "
                    % (r.status_code, counter, delay, method, url)
                )
                time.sleep(delay)
                continue
            if r.status_code == 401:
                if r.json().get("message") == "Unauthorized":
                    raise ApiUnauthorized("Unauthorized for this resource")
                raise r.raise_for_status()
            if r.status_code == 400:
                if r.json().get("error") == "Bad Request":
                    raise ApiQueueDoesNotExist("Queue does not exists")
                raise r.raise_for_status()
            if r.status_code == 404:
                raise r.raise_for_status()
            return r
