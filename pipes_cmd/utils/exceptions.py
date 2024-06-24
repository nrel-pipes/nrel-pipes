import grpc
import sys
import functools

def grpc_exception_handling(method):

    # preserves docs and name of method being decorated 
    @functools.wraps(method)

    # any of the PIPES methods can take an arbitrary # of positional or keyword args
    def inner_function(*args, **kwargs): 

        try:
            return method(*args, **kwargs)

        except grpc.RpcError as rpc_error:
            return {
                "code" : rpc_error.code().name,
                "details" : rpc_error.details()
            }
            
    return inner_function