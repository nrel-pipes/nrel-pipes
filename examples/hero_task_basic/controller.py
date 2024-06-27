import random
import pandas as pd

from hero import Hero
from pipes.sdk.core import Pipes

random.seed(0)

pipes = Pipes()

def get_modelrun_task():
    # Implement logic to pull modelrun
    modelrun = pipes.get_modelrun()
    return modelrun


if __name__ == "__main__":

    NUM_TASKS = 100

    # clear the queue
    hero = Hero()
    hero.clear_tasks()

    # push items
    modelrun = get_modelrun_task()
    task_ids = hero.put_tasks([modelrun])
    print(task_ids)

    # TODO: implement logics
    results = hero.wait_for_tasks(task_ids)
    print("tasks done")

    # send the exit signal to workers
    hero.send_exit_key_value('exit', True, num_tasks=10)

    # get results
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
