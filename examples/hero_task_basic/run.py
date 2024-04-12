import time
import os
import signal
import subprocess

WORKERS = 2

try:
    # launch the controller
    controller = subprocess.Popen(
        ['python', 'hero_controller.py'], 
        env=os.environ
    )

    time.sleep(5)
    # lanch the workers
    workers = subprocess.Popen(
        f"mpirun -np {WORKERS} python hero_worker.py", 
        shell=True, 
        env=os.environ
    )
    
    controller.wait()
    workers.wait()

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    controller.send_signal(signal.SIGINT)
    workers.send_signal(signal.SIGINT)
