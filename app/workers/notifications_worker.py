import asyncio
import json

from contextlib import suppress
from loguru import logger

from utils import ws_connection_manager
from utils.redis_client import redis, Channels


async def notifications_worker(stop_event: asyncio.Event | None = None):
    pubsub = redis.pubsub()
    await pubsub.subscribe(Channels.NOTIFICATIONS)
    logger.info(f"Worker: subscribed to Redis channel '{Channels.NOTIFICATIONS}'")

    try:
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue

            try:
                data = json.loads(message["data"])
            except Exception as e:
                logger.exception(f"Worker: invalid JSON: {message['data']}")
                continue

            user_id = data.get("to")
            if user_id is None:
                logger.warning(f"Worker: missing 'to' in message: {data}")
                continue

            await ws_connection_manager.send_personal_message(user_id=user_id, message=data)

            if stop_event and stop_event.is_set():
                break

    finally:
        with suppress(Exception):
            await pubsub.unsubscribe(Channels.NOTIFICATIONS)
            await pubsub.close()

        logger.info("Worker: stopped.")