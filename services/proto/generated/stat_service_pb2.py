"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12stat-service.proto"&\n\x13GetPostStatsRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x04"%\n\x12GetTopPostsRequest\x12\x0f\n\x07sort_by\x18\x01 \x01(\t"\x14\n\x12GetTopUsersRequest"E\n\x14GetPostStatsResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\x12\r\n\x05views\x18\x02 \x01(\x04\x12\r\n\x05likes\x18\x03 \x01(\x04"*\n\x08PostInfo\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\x12\r\n\x05count\x18\x02 \x01(\x04"/\n\x13GetTopPostsResponse\x12\x18\n\x05posts\x18\x01 \x03(\x0b2\t.PostInfo"0\n\x08UserInfo\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x13\n\x0blikes_count\x18\x02 \x01(\x04"/\n\x13GetTopUsersResponse\x12\x18\n\x05users\x18\x01 \x03(\x0b2\t.UserInfo2\xbe\x01\n\x0bStatService\x12;\n\x0cGetPostStats\x12\x14.GetPostStatsRequest\x1a\x15.GetPostStatsResponse\x128\n\x0bGetTopPosts\x12\x13.GetTopPostsRequest\x1a\x14.GetTopPostsResponse\x128\n\x0bGetTopUsers\x12\x13.GetTopUsersRequest\x1a\x14.GetTopUsersResponseb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stat_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETPOSTSTATSREQUEST']._serialized_start = 22
    _globals['_GETPOSTSTATSREQUEST']._serialized_end = 60
    _globals['_GETTOPPOSTSREQUEST']._serialized_start = 62
    _globals['_GETTOPPOSTSREQUEST']._serialized_end = 99
    _globals['_GETTOPUSERSREQUEST']._serialized_start = 101
    _globals['_GETTOPUSERSREQUEST']._serialized_end = 121
    _globals['_GETPOSTSTATSRESPONSE']._serialized_start = 123
    _globals['_GETPOSTSTATSRESPONSE']._serialized_end = 192
    _globals['_POSTINFO']._serialized_start = 194
    _globals['_POSTINFO']._serialized_end = 236
    _globals['_GETTOPPOSTSRESPONSE']._serialized_start = 238
    _globals['_GETTOPPOSTSRESPONSE']._serialized_end = 285
    _globals['_USERINFO']._serialized_start = 287
    _globals['_USERINFO']._serialized_end = 335
    _globals['_GETTOPUSERSRESPONSE']._serialized_start = 337
    _globals['_GETTOPUSERSRESPONSE']._serialized_end = 384
    _globals['_STATSERVICE']._serialized_start = 387
    _globals['_STATSERVICE']._serialized_end = 577