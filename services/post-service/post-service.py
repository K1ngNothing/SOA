# gRPC
import grpc
from google.protobuf import timestamp_pb2
from generated.post_service_pb2 import *
from generated.post_service_pb2_grpc import PostServiceServicer, add_PostServiceServicer_to_server

# SQLAlchemy
from sqlalchemy import create_engine, delete, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    Mapped,
    mapped_column,
)

# Misc
from concurrent import futures
import os
import sys
import time

time.sleep(5)
Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL'))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    content = Column(String)


Base.metadata.create_all(engine)


def CheckPostFound(request,
                   post,
                   context: grpc.ServicerContext):
    if not post or post.content == "":
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return False
    if post.author_id != request.user_id:
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("Post was not created by this user")
        return False
    return True


class PostService(PostServiceServicer):
    def CreatePost(self,
                   request: CreatePostRequest,
                   context: grpc.ServicerContext):
        with Session() as session:
            post = Post(
                author_id=request.author_id,
                content=request.content
            )
            session.add(post)
            session.commit()
            return PostIdResponse(post_id=post.id)

    def UpdatePost(self,
                   request: UpdatePostRequest,
                   context: grpc.ServicerContext):
        with Session() as session:
            post = session.query(Post).filter_by(
                id=request.post_id).first()

            if not CheckPostFound(request, post, context):
                return StatusResponse(success=False)

            post.content = request.content
            session.commit()
            return StatusResponse(success=True)

    def DeletePost(self,
                   request: DeletePostRequest,
                   context: grpc.ServicerContext):
        with Session() as session:
            post = session.query(Post).get(request.post_id)

            if not CheckPostFound(request, post, context):
                return StatusResponse(success=False)

            session.delete(post)
            session.commit()

            return StatusResponse(success=True)

    def GetPostById(self,
                    request: GetPostByIdRequest,
                    context: grpc.ServicerContext):
        with Session() as session:
            post = session.query(Post).filter_by(
                id=request.post_id).first()

            if not CheckPostFound(request, post, context):
                return PostResponse()

            return PostResponse(
                post_id=post.id,
                author_id=post.author_id,
                content=post.content,
            )

    def GetPosts(self,
                 request: GetPostsRequest,
                 context: grpc.ServicerContext):
        user_id = request.user_id
        posts_read = request.posts_read
        want_to_read = request.want_to_read

        with Session() as session:
            posts = session.query(Post).filter_by(author_id=user_id).filter(
                Post.content != "").offset(posts_read).limit(want_to_read).all()

            return GetPostsResponse(
                posts=[
                    PostResponse(
                        post_id=post.id,
                        author_id=post.author_id,
                        content=post.content,
                    )
                    for post in posts
                ]
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PostServiceServicer_to_server(PostService(), server)
    port = os.environ["POST_SERVICE_PORT"]
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
