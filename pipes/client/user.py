from .base import PipesClientBase


class UserClient(PipesClientBase):

    def list_users(self):
        return self.get("api/users")

    def get_user(self, username):
        return self.get("api/users/detail", params={"email": username})

    def create_user(self, data):
        return self.post("api/users", data=data)
