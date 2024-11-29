#!/usr/bin/env python

import asyncio

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recognition.settings')
import django
django.setup()

from django.conf import settings
from redis import asyncio as aioredis
from websockets.asyncio.server import broadcast, serve, ServerConnection


CONNECTIONS = set()


async def handler(websocket: ServerConnection):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def process_events():
    """Listen to events in Redis and process them."""
    redis = aioredis.from_url(settings.CACHES['default']['LOCATION'])
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.FACES_DETECTION_TOPIC)
    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        payload = message["data"].decode()
        broadcast(CONNECTIONS, payload)


async def main():
    async with serve(handler, "0.0.0.0", 8888):
        await process_events()


if __name__ == "__main__":
    asyncio.run(main())
