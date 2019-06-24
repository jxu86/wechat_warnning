from wechat_sender import *
from wxpy import *
import redis
import argparse
import pytoml

class Server():
    def __init__(self, params):
        self._config = params['config']
        self._receivers = []
        
        self._bot = Bot(console_qr=True, cache_path=True)
        self.r = redis.Redis(
            host=self._config['redis_host'],
            port=self._config['redis_port'],
            password=self._config['redis_password'],
            decode_responses=True)
        print('subscribe_msg: {}'.format(self._config['subscribe_msg']))
        self.ps = self.r.pubsub()
        self.ps.subscribe([self._config['subscribe_msg']])  # 订阅消息

        self.get_receivers()


    def get_receivers(self):
        try:
            if 'friends' in self._config:
                self._receivers += [self._bot.friends().search(f)[0] for f in self._config['friends']]
            if 'groups' in self._config:
                self._receivers += [self._bot.groups().search(g)[0] for g in self._config['groups']]
            print('wechat receivers: {}'.format(self._receivers))
        except Exception as e:
            print('error: {}'.format(e))

    def handle_data(self, data):
        for friend in self._receivers:
            friend.send(data)
        
    def run(self):
        # 基于redis subscribe
        for item in self.ps.listen():  # 监听状态：有消息发布了就拿过来
            if item['type'] == 'message':
                try:
                    # data = json.loads(item['data'])
                    data = item['data']
                    print('redis subscribe data: {}'.format(data))
                    self.handle_data(data)
                except Exception as e:
                    print('ERROE: {}'.format(e))

def parse_config(config_path):
    with open(config_path) as f:
        config = pytoml.load(f)

    return config
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default='config.toml',
        help='Config file (default: \'config.toml\')')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    print('##main##')
    args = parse_args()
    print('args: {}'.format(args))
    config = parse_config(args.config)
    print('config: {}',config)
    server = Server(config)
    server.run()