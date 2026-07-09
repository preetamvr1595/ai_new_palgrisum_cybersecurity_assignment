import redis
from backend.core.config import settings
import json

class RedisManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisManager, cls).__new__(cls)
            cls._instance._store = {}
            cls._instance.use_memory = False
            try:
                cls._instance.client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=0,
                    decode_responses=True,
                    socket_timeout=1
                )
                cls._instance.client.ping()
            except (redis.ConnectionError, redis.exceptions.TimeoutError):
                cls._instance.use_memory = True
                print("WARNING: Redis connection failed. Falling back to in-memory store for local development.")
        return cls._instance
    
    def get(self, key: str):
        if self.use_memory:
            value = self._store.get(key)
        else:
            try:
                value = self.client.get(key)
            except redis.ConnectionError:
                value = self._store.get(key)
                
        if value:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        return None
        
    def set(self, key: str, value: any, expire: int = None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        if self.use_memory:
            self._store[key] = value
        else:
            try:
                self.client.set(name=key, value=value, ex=expire)
            except redis.ConnectionError:
                self._store[key] = value
        
    def delete(self, key: str):
        if self.use_memory:
            self._store.pop(key, None)
        else:
            try:
                self.client.delete(key)
            except redis.ConnectionError:
                self._store.pop(key, None)
        
    def ping(self) -> bool:
        if self.use_memory:
            return True
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False

redis_client = RedisManager()
