import os
from time import time

import boto3
import jwt

from pipes.config import ClientConfig
from pipes.exception import InvalidToken
from pipes.session import Session


cognito_idp = boto3.client("cognito-idp", region_name="us-west-2")


def initiate_auth(username, password, aws=False):
    """Get Cognit access token for Bearer authentication"""
    if not aws:
        config = ClientConfig()
        response = cognito_idp.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=config.pipes_cognito,
        )
    else:
        response = cognito_idp.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=os.environ.get("PIPES_COGNITO_CLIENT_ID"),
        )

    token = response["AuthenticationResult"]["AccessToken"]
    return token


def validate_session_token():
    session = Session()
    token = session.data.get("token", None)
    if not token:
        print("Session token None")
        return False

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        current_time = int(time())
        exp_time = decoded_token.get('exp')
        if exp_time and current_time < exp_time:
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def get_access_token():
    session = Session()
    token = session.data.get("token", None)
    return token
