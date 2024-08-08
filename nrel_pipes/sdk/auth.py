import base64
import os
from dotenv import load_dotenv
import boto3
import jwt
from time import time
from .resilient_session import ResilientSession
from .config import PIPES_CLIENT_ID, HERO_COGNITO_API_URL
load_dotenv()


cognito_idp = boto3.client("cognito-idp", region_name="us-west-2")


def get_user_attributes(access_token):
    """Retrieve user attributes using the Access Token"""
    cognito_idp = boto3.client('cognito-idp')

    response = cognito_idp.get_user(
        AccessToken=access_token
    )
    
    return response['UserAttributes']


def get_pipes_token(username, password, client_id=PIPES_CLIENT_ID):
    """Get Cognit access token for Bearer authentication"""
    response = cognito_idp.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
        ClientId=client_id,
    )
    access_token = response["AuthenticationResult"]["AccessToken"]
    return access_token


def get_hero_token(client_id, client_secret, scopes):
    """
    Login to the Cognito user pool. Requires a client with a client secret and authorization to assign requested scopes.
    Returns a JWT access token.
    """
    app_client_id_secret = f"{client_id}:{client_secret}".encode("utf-8")
    # Request access_token following client credentials grant flow
    basic_auth = f"Basic {base64.urlsafe_b64encode(app_client_id_secret).decode()}"

    s = ResilientSession()
    response = s.post(
        HERO_COGNITO_API_URL,
        data=f'grant_type=client_credentials&scope={" ".join(scopes)}&client_id={client_id}',
        headers={
            "Authorization": basic_auth,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        verify=False,
    )
    response.raise_for_status()

    return response.json()["access_token"]


def valid_cognito_token(token):
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
    print(get_pipes_token(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))