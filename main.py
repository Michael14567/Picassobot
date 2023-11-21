import asyncio
import os
import aiohttp
import json
from typing import Dict, Any
import random
print("he")

import asyncio
from Tgclient import TgClient
from worker import Worker
from poller import Poller

async def main():
    token = "6772341949:AAGCojWTYAeT-vWRbC9ygYyw7B2PCH-PAtk"
    tg_client = TgClient(token)

    await tg_client.start()

    queue = asyncio.Queue()

    poller = Poller(tg_client, queue)
    worker = Worker(tg_client, queue)

    poller_task = asyncio.create_task(poller.poll())
    worker_task = asyncio.create_task(worker.start())

    await asyncio.gather(poller_task, worker_task)

    await tg_client.close()

if __name__ == "__main__":
    asyncio.run(main())