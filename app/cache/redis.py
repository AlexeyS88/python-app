import json

from redis import Redis
from redis.typing import EncodableT, KeyT

class RedisCacheBackend:
    def __init__(self, redis_url: str, cache_ttl_seconds: int | None = None) -> None:
        self.redis = Redis.from_url(url=redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds

    def set(self, key: KeyT, value: EncodableT) -> None:
        self.redis.set(key, value, ex=self.cache_ttl_seconds)

    def get(self, key: KeyT) -> EncodableT | None:
        data = self.redis.get(key)
        if data is not None:
            return json.loads(data)

    def delete(self, key: KeyT) -> None:
        self.redis.delete(key)
