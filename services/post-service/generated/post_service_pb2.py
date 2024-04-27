"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12post-service.proto\x12\x0bpostservice"7\n\x11CreatePostRequest\x12\x11\n\tauthor_id\x18\x01 \x01(\r\x12\x0f\n\x07content\x18\x02 \x01(\t"F\n\x11UpdatePostRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\r\x12\x0f\n\x07post_id\x18\x02 \x01(\r\x12\x0f\n\x07content\x18\x03 \x01(\t"5\n\x11DeletePostRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\r\x12\x0f\n\x07post_id\x18\x02 \x01(\r"6\n\x12GetPostByIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\r\x12\x0f\n\x07post_id\x18\x02 \x01(\r"L\n\x0fGetPostsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\r\x12\x12\n\nposts_read\x18\x02 \x01(\r\x12\x14\n\x0cwant_to_read\x18\x03 \x01(\r"!\n\x0ePostIdResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\r"!\n\x0eStatusResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08"C\n\x0cPostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\r\x12\x11\n\tauthor_id\x18\x02 \x01(\r\x12\x0f\n\x07content\x18\x03 \x01(\t"<\n\x10GetPostsResponse\x12(\n\x05posts\x18\x01 \x03(\x0b2\x19.postservice.PostResponse2\x8c\x03\n\x0bPostService\x12K\n\nCreatePost\x12\x1e.postservice.CreatePostRequest\x1a\x1b.postservice.PostIdResponse"\x00\x12K\n\nUpdatePost\x12\x1e.postservice.UpdatePostRequest\x1a\x1b.postservice.StatusResponse"\x00\x12K\n\nDeletePost\x12\x1e.postservice.DeletePostRequest\x1a\x1b.postservice.StatusResponse"\x00\x12K\n\x0bGetPostById\x12\x1f.postservice.GetPostByIdRequest\x1a\x19.postservice.PostResponse"\x00\x12I\n\x08GetPosts\x12\x1c.postservice.GetPostsRequest\x1a\x1d.postservice.GetPostsResponse"\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'post_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_CREATEPOSTREQUEST']._serialized_start = 35
    _globals['_CREATEPOSTREQUEST']._serialized_end = 90
    _globals['_UPDATEPOSTREQUEST']._serialized_start = 92
    _globals['_UPDATEPOSTREQUEST']._serialized_end = 162
    _globals['_DELETEPOSTREQUEST']._serialized_start = 164
    _globals['_DELETEPOSTREQUEST']._serialized_end = 217
    _globals['_GETPOSTBYIDREQUEST']._serialized_start = 219
    _globals['_GETPOSTBYIDREQUEST']._serialized_end = 273
    _globals['_GETPOSTSREQUEST']._serialized_start = 275
    _globals['_GETPOSTSREQUEST']._serialized_end = 351
    _globals['_POSTIDRESPONSE']._serialized_start = 353
    _globals['_POSTIDRESPONSE']._serialized_end = 386
    _globals['_STATUSRESPONSE']._serialized_start = 388
    _globals['_STATUSRESPONSE']._serialized_end = 421
    _globals['_POSTRESPONSE']._serialized_start = 423
    _globals['_POSTRESPONSE']._serialized_end = 490
    _globals['_GETPOSTSRESPONSE']._serialized_start = 492
    _globals['_GETPOSTSRESPONSE']._serialized_end = 552
    _globals['_POSTSERVICE']._serialized_start = 555
    _globals['_POSTSERVICE']._serialized_end = 951