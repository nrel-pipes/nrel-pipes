import os


HERO_CLIENT_ID = os.environ.get("HERO_CLIENT_ID")
HERO_COGNITO_API_URL = os.environ.get("HERO_COGNITO_API_URL")
HERO_CLIENT_SECRET = os.environ.get("HERO_CLIENT_SECRET")
HERO_TASK_ENGINE_API_URL = os.environ.get("HERO_TASK_ENGINE_API_URL")
HERO_QUEUE_ID = os.environ.get("HERO_QUEUE_ID")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
CLIENT_ID = os.environ.get("PIPES_CLIENT_KEY")
SCOPES = ["task-engine/user"]
PIPES_CLIENT_ID = os.environ.get("PIPES_COGNITO_CLIENT_ID")
HERO_DATA_HUB_PROJECT = os.environ.get("HERO_DATA_HUB_PROJECT")

HERO_DATA_HUB_PROJECT
READY = "ready"
CLAIMED = "claimed"
DONE = "done"
FAILED = "failed"
ACTIVE = "active"
DELETED = "deleted"

task_engine_id = "dev-nrel-kg"
