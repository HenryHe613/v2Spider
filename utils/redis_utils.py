import os
import redis
import threading


def init_redis():
    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    return r


class RedisUtils:
    _instance = None
    _lock = threading.Lock()  # 类级锁
    _initialized = False      # 类级初始化标记
    
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        with RedisUtils._lock:  # 使用锁保护初始化过程
            if not RedisUtils._initialized:
                host = os.getenv('REDIS_HOST')
                port = os.getenv('REDIS_PORT')
                db = os.getenv('REDIS_DB')
                password = os.getenv('REDIS_PASSWORD', None)
                unix_socket_path = os.getenv('REDIS_SOCKET_PATH')
                
                # 连接参数
                connection_kwargs = {
                    'db': int(db),
                    'password': password,
                    'decode_responses': False,  # 保持原始数据类型
                    'socket_timeout': 40,
                    'socket_connect_timeout': 40,
                    'retry_on_timeout': True,
                    'max_connections': 100
                }
                
                # 优先使用Unix套接字
                if unix_socket_path and os.path.exists(unix_socket_path):
                    self.__pool = redis.ConnectionPool(
                        unix_socket_path=unix_socket_path,
                        **connection_kwargs
                    )
                else:
                    # 回退到TCP连接
                    self.__pool = redis.ConnectionPool(
                        host=host,
                        port=int(port),
                        **connection_kwargs
                    )
                    
                self.__redis = redis.Redis(connection_pool=self.__pool)
                RedisUtils._initialized = True
                self.pipe = self.__redis.pipeline()
    
    def __del__(self):
        self.__pool.disconnect()
    
