from ast import List
import asyncio
import os
import threading
from typing import AsyncGenerator
import strawberry
from django.core.serializers import deserialize, serialize
from main.graphql.types import TmpType

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def on_message(self, info) -> str:
        print("starting on_message")
        print(id(info.context.broadcast))

        async with info.context.broadcast.subscribe(channel="chatroom") as subscriber:
            print(f"{subscriber=}")
            async for event in subscriber:
                print(f"{event=}")
                yield event.message

    @strawberry.subscription
    async def count(self, target: int = 100) -> int:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)
    @strawberry.subscription
    async def changed_hero(self, info) -> TmpType:
        async with info.context.broadcast.subscribe(channel="heros") as subscriber:
            async for event in subscriber:
                instance = list(deserialize("json", event.message))[0].object
                # yield instance
                yield TmpType(instance.name, instance.description)