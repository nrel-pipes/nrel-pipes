a = {
  "description": "this is team one",
  "members": [
    {
      "email": "user1@example.com",
      "first_name": "User1",
      "last_name": "Test",
      "organization": "Org1"
    },
    {
      "email": "user2@example.com",
      "first_name": "User2",
      "last_name": "Test",
      "organization": "Org2"
    }
  ],
  "name": "team1"
}


import toml

with open('team-creation.toml', "w") as f:
        team = toml.dump(a, f)
