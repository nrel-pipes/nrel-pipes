import json
from google.protobuf.json_format import MessageToDict
from pprint import pprint

def message_to_dict(message):
    """Convert grpc message to dictionary"""
    return MessageToDict(message, preserving_proto_field_name=True)


def print_response(response):
    """
    Print response to stdout console

    Parameters
    ----------
    response : Any
        dict or grpc response
    """
    # if response is None:
    #     print("No response")
    #     return

    # if not isinstance(response, dict):
    #     response = message_to_dict(response)

    # result = json.dumps(response, indent=2)

    pprint(response)
