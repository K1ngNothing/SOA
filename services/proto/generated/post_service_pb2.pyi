from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class CreatePostRequest(_message.Message):
    __slots__ = ['author_id', 'content']
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    author_id: int
    content: str

    def __init__(self, author_id: _Optional[int]=..., content: _Optional[str]=...) -> None:
        ...

class UpdatePostRequest(_message.Message):
    __slots__ = ['user_id', 'post_id', 'content']
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    post_id: int
    content: str

    def __init__(self, user_id: _Optional[int]=..., post_id: _Optional[int]=..., content: _Optional[str]=...) -> None:
        ...

class DeletePostRequest(_message.Message):
    __slots__ = ['user_id', 'post_id']
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    post_id: int

    def __init__(self, user_id: _Optional[int]=..., post_id: _Optional[int]=...) -> None:
        ...

class GetPostByIdRequest(_message.Message):
    __slots__ = ['user_id', 'post_id']
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    post_id: int

    def __init__(self, user_id: _Optional[int]=..., post_id: _Optional[int]=...) -> None:
        ...

class GetPostsRequest(_message.Message):
    __slots__ = ['user_id', 'posts_read', 'want_to_read']
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    POSTS_READ_FIELD_NUMBER: _ClassVar[int]
    WANT_TO_READ_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    posts_read: int
    want_to_read: int

    def __init__(self, user_id: _Optional[int]=..., posts_read: _Optional[int]=..., want_to_read: _Optional[int]=...) -> None:
        ...

class PostIdResponse(_message.Message):
    __slots__ = ['post_id']
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int

    def __init__(self, post_id: _Optional[int]=...) -> None:
        ...

class StatusResponse(_message.Message):
    __slots__ = ['success']
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool

    def __init__(self, success: bool=...) -> None:
        ...

class PostResponse(_message.Message):
    __slots__ = ['post_id', 'author_id', 'content']
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    author_id: int
    content: str

    def __init__(self, post_id: _Optional[int]=..., author_id: _Optional[int]=..., content: _Optional[str]=...) -> None:
        ...

class GetPostsResponse(_message.Message):
    __slots__ = ['posts']
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[PostResponse]

    def __init__(self, posts: _Optional[_Iterable[_Union[PostResponse, _Mapping]]]=...) -> None:
        ...