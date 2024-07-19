from pathlib import Path

# AWS
AWS_DEFAULT_REGION = "us-west-2"

GCP_LOCATION = "us-west1"


# PIPES
PIPES_CONFIG_DIRECTORY = str(Path.home() / ".pipes")

PIPES_SESSIONS_DIRECTORY = str(Path.home() / ".pipes" /"sessions")

PIPES_SETTINGS_FILE = str(Path.home() / ".pipes" / "settings")

PIPES_SESSION_EXPIRE = 3600 * 24 * 365 * 10  # In seconds

PIPES_API_URL = "https://localhost:8080/"

PIPES_CLIENT_ID = "6n5co9eh7bab4a21egr95ds3r8"