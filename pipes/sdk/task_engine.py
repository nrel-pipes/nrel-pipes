# """
# Steps to create task engine
# """

import requests
from dotenv import load_dotenv
import os, json
import logging
from .auth import get_pipes_token, get_hero_token
from .resilient_session import ResilientSession
load_dotenv()

READY = "ready"
CLAIMED = "claimed"
DONE = "done"
FAILED = "failed"
ACTIVE = "active"
DELETED = "deleted"

task_engine_id = "dev-nrel-kg"

HERO_QUEUE_ID = os.getenv("HERO_QUEUE_ID")
HERO_CLIENT_ID = os.getenv("HERO_CLIENT_ID")
HERO_CLIENT_SECRET = os.getenv("HERO_CLIENT_SECRET")
HERO_TASK_ENGINE_API_URL = os.getenv("HERO_TASK_ENGINE_API_URL")
HERO_DATA_HUB_PROJECT = os.getenv("HERO_DATA_HUB_PROJECT")

SCOPES = ["task-engine/user"]


log = logging.getLogger("hero:auth:cognito")

COGNITO_AUTH_URL = (
    "https://dev-nrel-research.auth.us-west-2.amazoncognito.com/oauth2/token"
)

import urllib3

urllib3.disable_warnings()



class Queue:
    def __init__(self, task_engine_id=HERO_TASK_ENGINE_API_URL):
        self.task_engine_id = task_engine_id
        self.token = get_hero_token(
            client_id=os.getenv("HERO_CLIENT_ID"),
            client_secret=os.getenv("HERO_CLIENT_SECRET"),
            scopes=SCOPES
        )
        self.queue_id = os.getenv("HERO_QUEUE_ID")
        self.task_engine_url = os.getenv("HERO_TASK_ENGINE_API_URL")
    
    def get_or_create_queue(self):
        url = f"{self.task_engine_url}/{self.task_engine_id}/queue"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        attributes = {"name": os.environ.get("HERO_QUEUE_ID")}
        payload = json.dumps(attributes)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data

    def get_queues(self, state=ACTIVE):
        """
        Returns a random set of `limit` queues of a given `state`
        """
        assert state in [ACTIVE, DELETED]
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/queues/metatype/Queue"
        query_params = f"?name={self.queue_id}|{state}"
        url = url + query_params
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        s = ResilientSession()
        response = s.request("GET", url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data

    def get_active_queue(self):
        """
        There can only be one active queue for a given queue_name.  This returns
        that queue or None if an active queue doesn't exist.
        """
        queues = self.get_queues()
        print(queues)
        for queue in queues:
            if queue["name"] == self.queue_id:
                tmp = {
                    "id": queue["id"],
                    "name": queue["name"],
                    "queueUrl": queue["queueUrl"],
                    "status": 200
                }
                return tmp
        return {"status": 404}
            

class HeroTaskEngine:
    def __init__(self, task_engine_id=HERO_DATA_HUB_PROJECT):
        self.task_engine_id = task_engine_id
        self.token = get_hero_token(client_id=HERO_CLIENT_ID, client_secret=HERO_CLIENT_SECRET, scopes=SCOPES)

    def push_task(self, task):
        """
        Adds a task to the queue with queue_id
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/task"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}

        # ensure the task has the following minimum fields
        assert "queueId" in task and "metadata" in task and "inputs" in task and "name" in task

        payload = json.dumps(task)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        data["status_code"] = 200
        return data
    
    def get_tasks(self, state=READY):
        """ 
        Getting tasks from the queue
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{task_engine_id}/queue/{HERO_QUEUE_ID}/tasks"
        query_params = f"?metatype=Task&state={state}"
        url = url + query_params
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


    def update_task(self, task_id, task):
        """
        Updates the task status and results in dynamodb and steams to open search.
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/task/{task_id}"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}

        # ensure it has the following fields
        task["state"] = task.get("state", DONE)
        assert task["state"] in [DONE, READY, CLAIMED, FAILED]
        task["outputs"] = task.get("outputs", {})

        payload = json.dumps(task)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()


    def pull_task(self, metatype="Task", num_messages=1, visibility_timeout=60):
        """
        The API pulls a task from SQS, checks to ensure it has not been claimed,
        and returns the task.
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/tasks"
        query_params = f"?receive={num_messages}"
        query_params += f"&visibilityTimeout={visibility_timeout}"
        query_params += f"&queueId={HERO_QUEUE_ID}"
        query_params += f"&metatype={metatype}"
        url = url + query_params
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()






data = [{'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'ubxo'},
  'inputs': {'input1': 'nnkciy', 'input2': 'egmkit', 'input3': 'wyzvow'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'ihnj'},
  'inputs': {'input1': 'jielfh', 'input2': 'jyrlfr', 'input3': 'dtdmha'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'vjfu'},
  'inputs': {'input1': 'ojauqw', 'input2': 'ddkgzs', 'input3': 'knpkxw'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'ogbu'},
  'inputs': {'input1': 'yjrrlc', 'input2': 'qsnyrs', 'input3': 'xidgaf'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'zosj'},
  'inputs': {'input1': 'jwvnzv', 'input2': 'arywhg', 'input3': 'ssgsml'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'mdem'},
  'inputs': {'input1': 'ngqayx', 'input2': 'hzxgfn', 'input3': 'qnusmh'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'yhki'},
  'inputs': {'input1': 'kjtkka', 'input2': 'jsarth', 'input3': 'wsehgw'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'ehiw'},
  'inputs': {'input1': 'zxsyqe', 'input2': 'czqtzi', 'input3': 'pmgjhr'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'mgwg'},
  'inputs': {'input1': 'wvfoqs', 'input2': 'mwbmmo', 'input3': 'gmoftu'},
  'state': 'ready'},
 {'name': 's3',
  'queueId': HERO_QUEUE_ID,
  'metadata': {'foo': 'yywx'},
  'inputs': {'input1': 'inqlty', 'input2': 'ofprds', 'input3': 'lmguat'},
  'state': 'ready'}]


if __name__=="__main__":
    print(f"Hero Token {HERO_TOKEN}")
    q = Queue()
    print("\n Queue Pulled Created \n")
    te = TaskEngine()
    print(data[1])
    te.push_task(data[2])
    print("\n Task Added \n")
    task = te.pull_tasks()
    print("\n Task Pulled \n")
    print(task)
    task = task[0]
    print(task)
    te.update_task(task["id"], task)
    print("\n Task Updated \n")
    te.get_tasks()
    print("\n Tasks gotten \n")
