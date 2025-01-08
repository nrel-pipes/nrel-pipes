import base64
import requests
import os
from dotenv import load_dotenv
import boto3
import jwt
from time import time


load_dotenv()


SCOPES = ["task-engine/user"]
CLIENT_ID = os.environ.get("HERO_CLIENT_ID")
CLIENT_SECRET = os.environ.get("HERO_CLIENT_SECRET")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def get_cognito_api():
    return os.environ.get(
        "HERO_COGNITO_API_URL",
        os.environ.get("HERO_COGNITO_API_URL"),
    )

COGNITO_AUTH_URL = os.environ.get("HERO_COGNITO_API_URL")

def get_hero_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scopes=SCOPES):
    """
    Login to the Cognito user pool. Requires a client with a client secret and authorization to assign requested scopes.

    Returns a JWT access token.
    """
    app_client_id_secret = f"{client_id}:{client_secret}".encode("utf-8")
    basic_auth = f"Basic {base64.urlsafe_b64encode(app_client_id_secret).decode()}"

    response = requests.post(
        COGNITO_AUTH_URL,
        data=f'grant_type=client_credentials&scope={" ".join(scopes)}&client_id={client_id}',
        headers={
            "Authorization": basic_auth,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        verify=False,
    )

    return response.json()["access_token"]


cognito_idp = boto3.client("cognito-idp", region_name="us-west-2")

def get_cognito_access_token(username, password):
    """Get Cognit access token for Bearer authentication"""
    response = cognito_idp.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
        ClientId=os.environ.get("PIPES_COGNITO_CLIENT_ID"),
    )
    access_token = response["AuthenticationResult"]["AccessToken"]
    return access_token


def token_valid(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        current_time = int(time())
        exp_time = decoded_token.get('exp')
        if exp_time and current_time > exp_time:
            return False
        else:
            return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return True
    except jwt.InvalidTokenError:
        print("Invalid token")
        return True


if __name__=="__main__":
    print(get_hero_token(os.environ.get("HERO_CLIENT_ID"), os.environ.get("HERO_CLIENT_SECRET"), SCOPES))
    print(get_cognito_access_token(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))