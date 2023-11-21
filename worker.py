import asyncio
from typing import Dict, Any
from Tgclient import TgClient
from aiogram import types
from database import Database
from aiogram import types 

class Worker:
    def __init__(self, tg_client: TgClient, queue: asyncio.Queue):
        self.tg_client = tg_client
        self.queue = queue
        self.db = Database('my_database.db')

    async def start(self):
        while True:
            update = await self.queue.get()
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')

                if text == '/start':
                    await self.send_welcome(chat_id)
                elif text == 'Играть':
                    await self.start_game(chat_id)

    async def send_welcome(self, chat_id):
        welcome_text = (
            "   Добро пожаловать !  \n"
            "Тебе нужно будет угадать \n"
            "Какая картина написанна художником \n"
            "А какая сгенирированна  AI\n"
            "Вперед! открой меню и нажми ИГРАТЬ\n"
            "Ссылки:\n"
            "[Discord](https://discord.gg/GmGfbgWDWk)\n"
            "[Поддержка](https://t.me/Dnec4)"
        )
        photo_path = 'C:/Users/spiri/Desktop/bot/welcome.jpg'
        await self.tg_client.send_photo(chat_id, photo_path, welcome_text)