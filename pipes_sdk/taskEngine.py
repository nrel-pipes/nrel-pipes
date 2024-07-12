# """
# Steps to create task engine
# """

import requests
from dotenv import load_dotenv
import os, json
from auth import HERO_TOKEN


load_dotenv()
HERO_CLIENT_ID = os.environ.get("HERO_CLIENT_ID")
HERO_CLIENT_SECRET = os.environ.get("HERO_CLIENT_SECRET")
HERO_TASK_ENGINE_API_URL = os.environ.get("HERO_TASK_ENGINE_API_URL")
HERO_QUEUE_ID = os.environ.get("HERO_QUEUE_ID")


READY = "ready"
CLAIMED = "claimed"
DONE = "done"
FAILED = "failed"
ACTIVE = "active"
DELETED = "deleted"

task_engine_id = "dev-nrel-kg"


class Queue:
    def __init__(self, task_engine_id=task_engine_id):
        self.task_engine_id = task_engine_id

    # Create a queue but change to only get...
    def get_or_create_queue(self):
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/queue"
        print(f"URL: {url}")
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HERO_TOKEN}"}
        attributes = {"name": os.environ.get("HERO_QUEUE_NAME")}
        payload = json.dumps(attributes)
        response = requests.post(url, headers=headers, data=payload)
        print(response)
        return response.json()


class TaskEngine:
    def __init__(self, task_engine_id=task_engine_id):
        self.task_engine_id = task_engine_id

    def add_task(self, task):
        """
        Adds a task to the queue with queue_id
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/task"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HERO_TOKEN}"}

        # ensure the task has the following minimum fields
        assert "queueId" in task and "metadata" in task and "inputs" in task and "name" in task

        payload = json.dumps(task)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        print("Task Added")
        return response.json()
    
    def get_tasks(state=READY):
        """ 
        Getting tasks from the queue
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{task_engine_id}/queue/{HERO_QUEUE_ID}/tasks"
        query_params = f"?metatype=Task&state={state}"
        url = url + query_params
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HERO_TOKEN}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


    def update_task(self, task_id, task):
        """
        Updates the task status and results in dynamodb and steams to open search.
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/task/{task_id}"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HERO_TOKEN}"}

        # ensure it has the following fields
        task["state"] = task.get("state", DONE)
        assert task["state"] in [DONE, READY, CLAIMED, FAILED]
        task["outputs"] = task.get("outputs", {})

        payload = json.dumps(task)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()


    def pull_task(self, metatype="Task", messages=1, visibility_timeout=60):
        """
        The API pulls a task from SQS, checks to ensure it has not been claimed,
        and returns the task.
        """
        url = f"{HERO_TASK_ENGINE_API_URL}/{self.task_engine_id}/tasks"
        query_params = f"?receive={messages}"
        query_params += f"&visibilityTimeout={visibility_timeout}"
        query_params += f"&queueId={HERO_QUEUE_ID}"
        query_params += f"&metatype={metatype}"
        url = url + query_params
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HERO_TOKEN}"}
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
    te.add_task(data[2])
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
