"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from . import post_service_pb2 as post__service__pb2

class PostServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePost = channel.unary_unary('/postservice.PostService/CreatePost', request_serializer=post__service__pb2.CreatePostRequest.SerializeToString, response_deserializer=post__service__pb2.PostIdResponse.FromString)
        self.UpdatePost = channel.unary_unary('/postservice.PostService/UpdatePost', request_serializer=post__service__pb2.UpdatePostRequest.SerializeToString, response_deserializer=post__service__pb2.StatusResponse.FromString)
        self.DeletePost = channel.unary_unary('/postservice.PostService/DeletePost', request_serializer=post__service__pb2.DeletePostRequest.SerializeToString, response_deserializer=post__service__pb2.StatusResponse.FromString)
        self.GetPostById = channel.unary_unary('/postservice.PostService/GetPostById', request_serializer=post__service__pb2.GetPostByIdRequest.SerializeToString, response_deserializer=post__service__pb2.PostResponse.FromString)
        self.GetPosts = channel.unary_unary('/postservice.PostService/GetPosts', request_serializer=post__service__pb2.GetPostsRequest.SerializeToString, response_deserializer=post__service__pb2.GetPostsResponse.FromString)

class PostServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPostById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_PostServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreatePost': grpc.unary_unary_rpc_method_handler(servicer.CreatePost, request_deserializer=post__service__pb2.CreatePostRequest.FromString, response_serializer=post__service__pb2.PostIdResponse.SerializeToString), 'UpdatePost': grpc.unary_unary_rpc_method_handler(servicer.UpdatePost, request_deserializer=post__service__pb2.UpdatePostRequest.FromString, response_serializer=post__service__pb2.StatusResponse.SerializeToString), 'DeletePost': grpc.unary_unary_rpc_method_handler(servicer.DeletePost, request_deserializer=post__service__pb2.DeletePostRequest.FromString, response_serializer=post__service__pb2.StatusResponse.SerializeToString), 'GetPostById': grpc.unary_unary_rpc_method_handler(servicer.GetPostById, request_deserializer=post__service__pb2.GetPostByIdRequest.FromString, response_serializer=post__service__pb2.PostResponse.SerializeToString), 'GetPosts': grpc.unary_unary_rpc_method_handler(servicer.GetPosts, request_deserializer=post__service__pb2.GetPostsRequest.FromString, response_serializer=post__service__pb2.GetPostsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('postservice.PostService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class PostService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreatePost(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/postservice.PostService/CreatePost', post__service__pb2.CreatePostRequest.SerializeToString, post__service__pb2.PostIdResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdatePost(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/postservice.PostService/UpdatePost', post__service__pb2.UpdatePostRequest.SerializeToString, post__service__pb2.StatusResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeletePost(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/postservice.PostService/DeletePost', post__service__pb2.DeletePostRequest.SerializeToString, post__service__pb2.StatusResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPostById(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/postservice.PostService/GetPostById', post__service__pb2.GetPostByIdRequest.SerializeToString, post__service__pb2.PostResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPosts(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/postservice.PostService/GetPosts', post__service__pb2.GetPostsRequest.SerializeToString, post__service__pb2.GetPostsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)