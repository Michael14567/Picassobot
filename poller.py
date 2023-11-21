import asyncio
from typing import Dict, Any
from Tgclient import TgClient

class Poller:
    def __init__(self, tg_client: TgClient, queue: asyncio.Queue):
        self.tg_client = tg_client
        self.queue = queue

    async def poll(self):
        offset = 0
        while True:
            updates = await self.tg_client.get_updates(offset)
            if 'result' in updates:
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    await self.queue.put(update)