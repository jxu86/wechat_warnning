import redis
import json


subscribe_msg = 'wechat-warnning-test'  # config.toml subscribe_msg字段要一样
r = redis.Redis(host='127.0.0.1', port=6379,password='xxx', decode_responses=True)

# data = {
#     'receivers': [{
#         'type': 'friend',
#         'user': 'JC'
#     },
#     {
#         'type': 'group',
#         'user': 'warnning'
#     }],
#     'msg': 'hello world'
# }
r.publish('wechat-warnning-test', 'hi hi hi, test')

