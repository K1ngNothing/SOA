from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GetPostStatsRequest(_message.Message):
    __slots__ = ['post_id']
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int

    def __init__(self, post_id: _Optional[int]=...) -> None:
        ...

class GetTopPostsRequest(_message.Message):
    __slots__ = ['sort_by']
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    sort_by: str

    def __init__(self, sort_by: _Optional[str]=...) -> None:
        ...

class GetTopUsersRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetPostStatsResponse(_message.Message):
    __slots__ = ['post_id', 'views', 'likes']
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    views: int
    likes: int

    def __init__(self, post_id: _Optional[int]=..., views: _Optional[int]=..., likes: _Optional[int]=...) -> None:
        ...

class PostInfo(_message.Message):
    __slots__ = ['post_id', 'count']
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    count: int

    def __init__(self, post_id: _Optional[int]=..., count: _Optional[int]=...) -> None:
        ...

class GetTopPostsResponse(_message.Message):
    __slots__ = ['posts']
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[PostInfo]

    def __init__(self, posts: _Optional[_Iterable[_Union[PostInfo, _Mapping]]]=...) -> None:
        ...

class UserInfo(_message.Message):
    __slots__ = ['user_id', 'likes_count']
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LIKES_COUNT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    likes_count: int

    def __init__(self, user_id: _Optional[int]=..., likes_count: _Optional[int]=...) -> None:
        ...

class GetTopUsersResponse(_message.Message):
    __slots__ = ['users']
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserInfo]

    def __init__(self, users: _Optional[_Iterable[_Union[UserInfo, _Mapping]]]=...) -> None:
        ...