from redis import Redis

from settings import settings


redis = Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB, 
    decode_responses=True
)


class Channels:
    NOTIFICATIONS = "notifications"
