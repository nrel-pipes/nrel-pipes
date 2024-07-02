import time

from hero import Hero
from p.sdk.core import Pipes


def execute_modelrun(hero, task):
    pipes = Pipes()
    modelrun_name = task.inputs["name"]

    time.sleep(1)
    hero.update_task(task, {"results": "complete", "modelrun": modelrun_name})

    p.update_task(task, {"results": "complete", "modelrun": modelrun_name})


if __name__ == "__main__":

    # If after 45 attemps where there are no tasks, the worker will exit
    attempts = 0
    hero = Hero()

    while True:
        task = hero.pull_task(attempts=1)
        if task:
            if task.inputs.get('exit', False):
                exit()
            execute_modelrun(hero, task)
            attempts = 0
        else:
            attempts += 1
        hero.wait(1)

        if attempts > 45:
            break
