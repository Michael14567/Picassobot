import asyncio
import os
import sqlite3
import aiohttp
import json
from typing import Dict, Any
import random
print("he")

image_answers = {
    '0.jpeg': {'answer': 'Сгенирированная', 'description': 'Железная дорога', 'error_message': 'К сожалению её негде посмотреть  , она сгенирирована AI'},
    '1.jpg': {'answer': 'Сгенирированная', 'description': 'Синопское сражение', 'error_message': 'К сожалению ты не угадал(а) , этой картины никогда не было'},
    '2.jpg': {'answer': 'Сгенирированная', 'description': 'Аржантёй', 'error_message': 'Похоже на моне , но сгенерена AI'},
    '3.jpg': {'answer': 'Реальная', 'description': 'Портрет вице-адмирала ', 'error_message': ' И.К.Айвазовского 1839 Центральный военно-морской музей https://navalmuseum.ru/contact/ticket_price_filial/ticket_museum'},
    '4.jpg': {'answer': 'Сгенирированная', 'description': 'Морской берег', 'error_message': 'Жаль, это не Айвазовский ,а только AI'},
    '5.jpg': {'answer': 'Реальная', 'description': 'Букет цветов в сером кувшине', 'error_message': 'Пикассо  1908 год Коллекция: Санкт-Петербург, Государственный Эрмитаж https://www.hermitagemuseum.org/wps/portal/hermitage/tickets?lng=ru'},
    '6.jpg': {'answer': 'Реальная', 'description': 'Композиция VI', 'error_message': 'Василий Кандинский. Композиция VI Одно из самых известных творений мастера абстрактной живописи  — демонстрируется в зале № 444 Главного штаба. https://www.hermitagemuseum.org/wps/portal/hermitage/visitus/general-staff?lng=ru'},
    '7.jpg': {'answer': 'Реальная', 'description': 'Девятый вал', 'error_message': 'Масштабное полотно Ивана Айвазовского «Девятый вал», представленное Михайловском дворце в зале № 14 https://ticket.rusmuseum.ru/?id=1&sid=481'},
    '8.jpeg': {'answer': 'Реальная', 'description': 'Роспись на индийском красном фоне', 'error_message': 'Джексон Поллок к сожалению в Питере ее не получится увидеть в живую'},
    '9.jpg': {'answer': 'Реальная', 'description': 'Две читающие девушки', 'error_message': 'Пабло Пикассо.С 1994 года она находится в Музее искусств Мичиганского университета.'},
    '10.jpeg': {'answer': 'Сгенирированная', 'description': 'Букет цветов', 'error_message': 'Ai когда-нибудь заменит нас'},
    '11.jpg': {'answer': 'Реальная', 'description': 'Композиция VII', 'error_message': 'Василий Кандинский. 1913 год .Находится в собрании Третьяковской галереи в Москве.'},
    '12.jpeg': {'answer': 'Сгенирированная', 'description': 'Пикник трех солдат у Черной горы', 'error_message': 'Обрати внимание на глаз, AI пока не совершенна'},
    '13.jpg': {'answer': 'Сгенирированная', 'description': 'Трое за столом', 'error_message': 'Красивая картина , но AI'},
    '14.jpg': {'answer': 'Сгенирированная', 'description': 'Мечеть в Тунисе', 'error_message': 'У меня асоциация с дюной ,а у вас? AI'},
    '15.jpg': {'answer': 'Сгенирированная', 'description': 'Восхождение', 'error_message': 'Тут конечно очевидно , но инетересно . Да это тоже AI'},
    '16.jpg': {'answer': 'Сгенирированная', 'description': 'Молитва', 'error_message': 'Надо чуть внимательнее быть ) AI'},
    '17.jpg': {'answer': 'Сгенирированная', 'description': 'Девушка с кошкой', 'error_message': 'AI что тут сказать'},
    '18.jpg': {'answer': 'Сгенирированная', 'description': '----', 'error_message': 'не могу найти реальна ли картина или нет'},
    '19.jpg': {'answer': 'Сгенирированная', 'description': 'Композиция X', 'error_message': 'Я как-то по приколу сгенерил, AI'},
    '20.jpg': {'answer': 'Реальная', 'description': 'Мост Ватерлоо', 'error_message': 'Claude Monet 1903. Государственный Эрмитаж https://www.hermitagemuseum.org/wps/portal/hermitage/tickets?lng=ru'},
    '21.jpg': {'answer': 'Реальная', 'description': 'Мадонна Литта', 'error_message': 'Леонардо да Винчи Полотно представлено в зале № 214 Большого (Старого) Эрмитажа. https://www.hermitagemuseum.org/wps/portal/hermitage/tickets?lng=ru'},
    '22.jpg': {'answer': 'Реальная', 'description': 'Танец', 'error_message': '«Танец» и «Музыка» хранятся в зале № 440 Главного штаба, https://www.hermitagemuseum.org/wps/portal/hermitage/visitus/general-staff?lng=ru'},
    '23.jpg': {'answer': 'Реальная', 'description': 'После полудня, солнечно', 'error_message': 'Камиль Писсарро в зале № 406 Главного штаба https://www.hermitagemuseum.org/wps/portal/hermitage/visitus/general-staff?lng=ru'},
    '24.jpg': {'answer': 'Реальная', 'description': 'Портрет Иды Рубинштейн', 'error_message': 'Портрет можно увидеть в зале № 69 корпуса Бенуа. https://ticket.rusmuseum.ru/'},
    '25.jpg': {'answer': 'Реальная', 'description': 'Последний день Помпеи', 'error_message': 'Карл Брюллов Хранится в Государственном Русском музее в Санкт-Петербурге https://ticket.rusmuseum.ru/'},
    '26.jpg': {'answer': 'Реальная', 'description': 'Лунная ночь на Днепре', 'error_message': 'Архип Куинджи Государственный Русский музей https://ticket.rusmuseum.ru/'},
    '27.jpg': {'answer': 'Реальная', 'description': 'Небесный бой', 'error_message': 'Н. К. Рерих , Флигель России, зал № 41 Русский музей https://ticket.rusmuseum.ru/'},
    '28.jpg': {'answer': 'Реальная', 'description': 'Большая набережная в Гавре', 'error_message': 'Клод Моне 1874 Главного штаба https://www.hermitagemuseum.org/wps/portal/hermitage/visitus/general-staff?lng=ru'},
    '29.jpg': {'answer': 'Реальная', 'description': 'Сад в Бордигере, утро', 'error_message': 'Клод Моне  в здании Главного Штаба зал 403. https://www.hermitagemuseum.org/wps/portal/hermitage/visitus/general-staff?lng=ru'},
    '30.jpg': {'answer': 'Сгенирированная', 'description': 'Осень в Люблице', 'error_message': 'AI'},
    '31.jpg': {'answer': 'Сгенирированная', 'description': 'Замок', 'error_message': 'AI'},
    '32.jpg': {'answer': 'Сгенирированная', 'description': 'Сказочный замок', 'error_message': 'AI'},
    # и так далее для каждого изображения
}

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_image_answers_table(self):
        query = '''CREATE TABLE IF NOT EXISTS image_answers (
                       image_name TEXT PRIMARY KEY,
                       answer TEXT,
                       description TEXT,
                       error_message TEXT
                   )'''
        self.cursor.execute(query)
        self.conn.commit()
    
    def insert_image_answers(self, image_answers):
        for image_name, values in image_answers.items():
            answer = values['answer']
            description = values['description']
            error_message = values['error_message']
            query = f'''INSERT OR REPLACE INTO image_answers 
                        (image_name, answer, description, error_message) 
                        VALUES (?, ?, ?, ?)'''
            self.cursor.execute(query, (image_name, answer, description, error_message))
        self.conn.commit()
    
    def fetch_image_answer(self, image_name):
        query = '''SELECT * FROM image_answers WHERE image_name = ?'''
        self.cursor.execute(query, (image_name,))
        return self.cursor.fetchone()
    
    def get_random_image_name(self):
        query = '''SELECT image_name FROM image_answers'''
        self.cursor.execute(query)
        image_names = [row[0] for row in self.cursor.fetchall()]
        return random.choice(image_names)
    
    def close(self):
        self.conn.close()

# Пример использования:
db = Database('my_database.db')
db.create_image_answers_table()
db.insert_image_answers(image_answers)
# Для получения информации по определенному изображению:
result = db.fetch_image_answer('0.jpeg')
print(result)
db.close()

class TgClient:
    API_URL = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.token = token
        self.session = None

    async def start(self):
        print("Starting the Telegram client...")
        self.session = aiohttp.ClientSession()

    async def get_updates(self, offset: int = 0, timeout: int = 60) -> Dict[str, Any]:
        url = f"{self.API_URL}{self.token}/getUpdates?offset={offset}&timeout={timeout}"
        async with self.session.get(url) as response:
            data = await response.text()
            return json.loads(data)

    async def send_message(self, chat_id: int, text: str, reply_markup=None) -> Dict[str, Any]:
        url = f"{self.API_URL}{self.token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }

        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)

        async with self.session.post(url, data=payload) as response:
            data = await response.json()
            return data
        
    async def get_chat_id(self):
        updates = await self.get_updates()
        if 'result' in updates and updates['result']:
            chat_id = updates['result'][0]['message']['chat']['id']
            return chat_id
        return None
    async def close(self):
        if self.session:
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
    async def send_start_menu(self, chat_id):
        # Создание стартового меню с четырьмя кнопками
        start_menu = {
            'keyboard': [
                [{'text': 'Играть'}, {'text': 'Настройки'}],
                [{'text': 'Режимы'}, {'text': 'Смотреть'}]
            ],
            'resize_keyboard': True
        }
        await self.send_message(chat_id, "Выберите действие:", reply_markup=start_menu)
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
                    print("Received /start command")  # Add this line
                    await self.send_welcome(chat_id)
                elif text == 'Играть':
                    await self.start_game(chat_id)
            
            elif 'callback_query' in update:
                callback_data = update['callback_query']['data']
                chat_id = update['callback_query']['message']['chat']['id']

                if callback_data == 'play':
                    await self.start_game(chat_id)
                elif callback_data == 'settings':
                    await self.send_settings(chat_id)
                elif callback_data == 'modes':
                    await self.send_modes(chat_id)
                elif callback_data == 'watch':
                    await self.send_watch(chat_id)
    async def handle_callback(self, chat_id, callback_data):
        # Обработка данных от нажатых кнопок
        if callback_data == 'play':
            await self.start_game(chat_id)
        elif callback_data == 'settings':
            await self.send_settings(chat_id)
        elif callback_data == 'modes':
            await self.send_modes(chat_id)
        elif callback_data == 'watch':
            await self.send_watch(chat_id)
                    
    async def start_game(self, chat_id):
    # Получение случайного изображения из базы данных
        image_name = self.db.get_random_image_name()
        image_data = self.db.fetch_image_answer(image_name)

        if image_data:
            description = image_data[2]  # Описание изображения
            photo_path = f'C:/Users/spiri/Desktop/bot/{image_name}'  # Путь к изображению на сервере

            # Генерация кнопок
            buttons = self.generate_answer_buttons()

            # Отправка изображения с описанием и кнопками
            await self.tg_client.send_photo(chat_id, photo_path, description, reply_markup=buttons)

            # Ожидание ответа от пользователя
            user_choice = await self.wait_for_user_choice(chat_id)
            if user_choice:
                # Обработка выбора пользователя
                await self.handle_user_choice(chat_id, user_choice, image_data)
        else:
            await self.tg_client.send_message(chat_id, "Извините, произошла ошибка. Попробуйте снова.")

    def generate_answer_buttons(self):
        answer_buttons = {
            'inline_keyboard': [
                [{'text': 'Реальная', 'callback_data': 'real'}, {'text': 'Сгенерированная', 'callback_data': 'generated'}]
            ]
        }
        return answer_buttons
    async def wait_for_user_choice(self, chat_id):
        while True:
            updates = await self.tg_client.get_updates()
            if 'result' in updates:
                for update in updates['result']:
                    if 'callback_query' in update and update['callback_query']['message']['chat']['id'] == chat_id:
                        return update['callback_query']['data']
    async def handle_user_choice(self, chat_id, user_choice, image_data):
        correct_answer = image_data['answer']
        if user_choice == 'real' and correct_answer == 'Реальная':
            await self.tg_client.send_message(chat_id, "Верно! Следующая картинка.")
            # Повторение игры для следующего изображения
            await self.start_game(chat_id)
        elif user_choice == 'generated' and correct_answer == 'Сгенирированная':
            await self.tg_client.send_message(chat_id, "Верно! Следующая картинка.")
            # Повторение игры для следующего изображения
            await self.start_game(chat_id)
        else:
            error_message = image_data['error_message']
            await self.tg_client.send_message(chat_id, f"Неверно! Правильный ответ: {correct_answer}. {error_message}")
    async def send_welcome(self, chat_id):
        # Отправка изображения отдельно
        photo_path = 'C:/Users/spiri/Desktop/bot/welcome.jpg'
        await self.tg_client.send_photo(chat_id, photo_path)

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

        start_menu = {
            'inline_keyboard': [
                [{'text': 'Играть', 'callback_data': 'play'}],
                [{'text': 'Настройки', 'callback_data': 'settings'}],
                [{'text': 'Режимы', 'callback_data': 'modes'}],
                [{'text': 'Смотреть', 'callback_data': 'watch'}]
            ]
        }

        # Отправка только текста и кнопок через send_message
        await self.tg_client.send_message(chat_id, welcome_text, reply_markup=start_menu)

    async def send_settings(self, chat_id):
        # Заглушка для настроек
        await self.tg_client.send_message(chat_id, "Настройки - Заглушка")

    async def send_modes(self, chat_id):
        # Заглушка для режимов
        await self.tg_client.send_message(chat_id, "Режимы - Заглушка")

    async def send_watch(self, chat_id):
        # Заглушка для смотреть
        await self.tg_client.send_message(chat_id, "Смотреть - Заглушка")
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
async def main():
    token = "6772341949:AAFo-jFQ2xUNGY9dTxtBixsgVckyp4eanJc"
    tg_client = TgClient(token)

    print("Bot starting...")
    await tg_client.start()

    queue = asyncio.Queue()

    poller = Poller(tg_client, queue)
    worker = Worker(tg_client, queue)

    poller_task = asyncio.create_task(poller.poll())
    worker_task = asyncio.create_task(worker.start())
    test_chat_id = await tg_client.get_chat_id()
    if test_chat_id:
        print(f"Chat ID: {test_chat_id}")

    if test_chat_id:
        await tg_client.send_start_menu(test_chat_id)
    print("Sending start menu...")
    await tg_client.send_start_menu(test_chat_id)
    
    # Переносим начало опроса после отправки стартового меню
    await asyncio.gather(poller_task, worker_task)

    await tg_client.close()

if __name__ == "__main__":
    asyncio.run(main())