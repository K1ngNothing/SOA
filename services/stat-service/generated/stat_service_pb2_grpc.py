"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from . import stat_service_pb2 as stat__service__pb2

class StatServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPostStats = channel.unary_unary('/StatService/GetPostStats', request_serializer=stat__service__pb2.GetPostStatsRequest.SerializeToString, response_deserializer=stat__service__pb2.GetPostStatsResponse.FromString)
        self.GetTopPosts = channel.unary_unary('/StatService/GetTopPosts', request_serializer=stat__service__pb2.GetTopPostsRequest.SerializeToString, response_deserializer=stat__service__pb2.GetTopPostsResponse.FromString)
        self.GetTopUsers = channel.unary_unary('/StatService/GetTopUsers', request_serializer=stat__service__pb2.GetTopUsersRequest.SerializeToString, response_deserializer=stat__service__pb2.GetTopUsersResponse.FromString)

class StatServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetPostStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_StatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'GetPostStats': grpc.unary_unary_rpc_method_handler(servicer.GetPostStats, request_deserializer=stat__service__pb2.GetPostStatsRequest.FromString, response_serializer=stat__service__pb2.GetPostStatsResponse.SerializeToString), 'GetTopPosts': grpc.unary_unary_rpc_method_handler(servicer.GetTopPosts, request_deserializer=stat__service__pb2.GetTopPostsRequest.FromString, response_serializer=stat__service__pb2.GetTopPostsResponse.SerializeToString), 'GetTopUsers': grpc.unary_unary_rpc_method_handler(servicer.GetTopUsers, request_deserializer=stat__service__pb2.GetTopUsersRequest.FromString, response_serializer=stat__service__pb2.GetTopUsersResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('StatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class StatService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetPostStats(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/StatService/GetPostStats', stat__service__pb2.GetPostStatsRequest.SerializeToString, stat__service__pb2.GetPostStatsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTopPosts(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/StatService/GetTopPosts', stat__service__pb2.GetTopPostsRequest.SerializeToString, stat__service__pb2.GetTopPostsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTopUsers(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/StatService/GetTopUsers', stat__service__pb2.GetTopUsersRequest.SerializeToString, stat__service__pb2.GetTopUsersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)