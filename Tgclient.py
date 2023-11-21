import aiohttp
import json
from typing import Dict, Any

class TgClient:
    API_URL = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.token = token
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def get_updates(self, offset: int = 0, timeout: int = 60) -> Dict[str, Any]:
        url = f"{self.API_URL}{self.token}/getUpdates?offset={offset}&timeout={timeout}"
        async with self.session.get(url) as response:
            data = await response.text()
            return json.loads(data)

    async def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        url = f"{self.API_URL}{self.token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with self.session.post(url, data=payload) as response:
            data = await response.json()
            return data

    async def close(self):
        await self.session.close()

    async def send_photo(self, chat_id: int, photo_path: str, caption: str = '', reply_markup=None) -> Dict[str, Any]:
        url = f"{self.API_URL}{self.token}/sendPhoto"
        data = aiohttp.FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('photo', open(photo_path, 'rb'))
        data.add_field('caption', caption)

        if reply_markup:
            # Assuming reply_markup is properly formatted as InlineKeyboardMarkup
            data.add_field('reply_markup', json.dumps(reply_markup))

        async with self.session.post(url, data=data) as response:
            return await response.json()
