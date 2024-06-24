from pipes_cmd.config.settings import ClientSettings
from pipes_cmd.config.session import get_token
from pipes_sdk import PipesClient

settings = ClientSettings()
TOKEN = get_token()
CLIENT = PipesClient(url=settings.get_server(), token=TOKEN)
