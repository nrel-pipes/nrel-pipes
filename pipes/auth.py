import time
import os
import jwt
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from pipes.config import ClientConfig
from pipes.exception import InvalidToken
from pipes.session import Session


cognito_idp = boto3.client("cognito-idp", region_name="us-west-2")


def create_boto3_session():
    """Create a boto3 session with credentials from environment variables or default credential chain."""
    try:
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
        aws_region = os.environ.get('AWS_REGION', 'us-west-2')

        if aws_access_key_id and aws_secret_access_key:
            print("Creating boto3 session with explicit AWS credentials from environment variables.")
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=aws_region
            )
        else:
            print("Creating boto3 session using default AWS credential chain.")
            session = boto3.Session(region_name=aws_region)
        return session
    except Exception as e:
        print(f"Failed to create boto3 session: {e}")
        raise

def get_ssm_parameter(parameter_name):
    """Fetch a parameter from AWS Systems Manager (SSM) Parameter Store."""
    try:
        session = create_boto3_session()
        ssm_client = session.client('ssm')
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        print(f"Successfully retrieved parameter: {parameter_name}")
        return response['Parameter']['Value']
    except NoCredentialsError:
        print("No valid AWS credentials found.")
        return None
    except ClientError as e:
        print(f"An error occurred while fetching the SSM parameter: {e}")
        return None

def validate_token(token):
    """Validate the token against the Cognito User Pool and return a boolean."""
    try:
        session = create_boto3_session()
        cognito_client = session.client('cognito-idp')
        cognito_client.get_user(AccessToken=token)
        print("Token is valid.")
        return True
    except cognito_client.exceptions.NotAuthorizedException as e:
        print(f"Token validation failed: {e}")
        return False
    except ClientError as e:
        print(f"An error occurred while validating the token: {e}")
        return False

def refresh_access_token(client_id, refresh_token):
    """Use the refresh token to get a new access token."""
    try:
        session = create_boto3_session()
        cognito_client = session.client('cognito-idp')
        response = cognito_client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': refresh_token},
            ClientId=client_id
        )
        new_access_token = response['AuthenticationResult']['AccessToken']
        print("Successfully refreshed the access token.")
        return new_access_token
    except cognito_client.exceptions.NotAuthorizedException as e:
        print(f"Refresh token authentication failed: {e}")
        return None
    except ClientError as e:
        print(f"An error occurred while refreshing the token: {e}")
        return None

def store_token_in_ssm(parameter_name, token):
    """Store the token in AWS Systems Manager (SSM) Parameter Store."""
    try:
        session = create_boto3_session()
        ssm_client = session.client('ssm')
        ssm_client.put_parameter(
            Name=parameter_name,
            Value=token,
            Type='SecureString',
            Overwrite=True
        )
        print(f"Successfully stored the token in SSM under {parameter_name}.")
    except ClientError as e:
        print(f"An error occurred while storing the token in SSM: {e}")
        raise

def cloud_auth():
    token_param_name = '/nrel/pipes-hero/dev/TOKEN'
    refresh_token_param_name = '/nrel/pipes-hero/dev/REFRESH_TOKEN'
    client_id = os.environ.get("COGNITO_CLIENT_ID")

    print("Starting token management process...")

    if not client_id:
        print("Error: COGNITO_CLIENT_ID environment variable is not set.")
        return

    # Step 1: Get the access token from SSM
    access_token = get_ssm_parameter(token_param_name)
    if not access_token:
        print("Failed to retrieve access token from SSM.")
        return

    # Step 2: Validate the access token
    if not validate_token(access_token):
        print("Access token is invalid. Attempting to refresh it.")

        # Step 3: Get the refresh token from SSM
        refresh_token = get_ssm_parameter(refresh_token_param_name)
        if not refresh_token:
            print("Failed to retrieve refresh token from SSM.")
            return

        # Step 4: Attempt to refresh the access token
        new_access_token = refresh_access_token(client_id, refresh_token)

        if new_access_token:
            # Step 5: Store the new access token in SSM
            store_token_in_ssm(token_param_name, new_access_token)
            print("Token refresh process completed successfully.")
        else:
            print("Failed to refresh the token. Manual intervention may be required.")
    else:
        print("Access token is valid. No action needed.")

    print("Token management process completed.")



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
