import os
import random
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

# Создание соединения и курсора для работы с базой данных
conn = sqlite3.connect('Картины.db')
cursor = conn.cursor()

# Создание таблицы image_answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS image_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT UNIQUE,
        answer TEXT,
        description TEXT,
        error_message TEXT
    )
''')

# Пример заполнения таблицы данными (замените этот код вашими данными)
image_answers_data = {
    '0.jpeg': {'answer': 'Сгенирированная', 'description': 'Железная дорога', 'error_message': 'К сожалению её негде посмотреть  , она сгенирирована AI '},
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
# Вставляем данные в таблицу
cursor.executemany('''
    INSERT INTO image_answers (image_name, answer, description, error_message)
    VALUES (?, ?, ?, ?)
''', image_answers_data)

# Подтверждаем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()
# Подключение к базе данных
API_TOKEN = '6772341949:AAFo-jFQ2xUNGY9dTxtBixsgVckyp4eanJc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

image_folder = 'C:/Users/spiri/Desktop/bot'
# Остальные переменные и словари остаются такими же, как в вашем предыдущем коде

# Ваши словари и переменные остаются неизменными
image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]



# Список для хранения ошибок
user_errors = []

# Создаем кнопки для главного меню
play_button = types.KeyboardButton("Играть")
watch_button = types.KeyboardButton("Смотреть")
setting_button = types.KeyboardButton("Настройки")
rating_button = types.KeyboardButton("Рейтинг")

# Создаем главное меню
main_menu_markup = types.ReplyKeyboardMarkup(row_width=2)
main_menu_markup.add(play_button,rating_button,setting_button,watch_button)

current_image = None  # Текущее изображение
# Заменяем функции telebot на аналогичные функции из aiogram
# Создаем кнопки "Реальная" и "Сгенирированная"
left_button = types.KeyboardButton("Реальная")
right_button = types.KeyboardButton("Сгенирированная")

# Создаем меню с этими кнопками
markup = types.ReplyKeyboardMarkup(row_width=2)
markup.add(left_button, right_button)

user_score = 0
current_round = 0
available_images = []  # Список доступных изображений
# Ваша функция для отправки приветственного сообщения
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "(ﾉ◕ヮ◕)ﾉ Добро пожаловать !  \n"
        "Тебе нужно будет угадать \n"
        "Какая картина написанна художником \n"
        "А какая сгенерирована AI\n"
        "Вперед! открой меню и нажми СТАРТ\n"
        "[Discord](https://discord.gg/GmGfbgWDWk)\n"
        "[Поддержка](https://t.me/Dnec4)\n"
    )
    welcome_image_path = os.path.join(image_folder, 'welcome.jpg')

    # Создаем клавиатуру с кнопками inline
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Старт", callback_data="start"),
        InlineKeyboardButton("Режим", callback_data="mode"),
        InlineKeyboardButton("Настройки", callback_data="settings"),
        InlineKeyboardButton("Смотреть", callback_data="watch")
    )

    with open(welcome_image_path, 'rb') as welcome_image:
        await message.answer_photo(welcome_image, caption=welcome_text, reply_markup=keyboard)

# Остальные функции также адаптируются для использования асинхронных методов из aiogram
# Например, функция для отправки изображения может выглядеть так:
# Добавляем обработку callback-запроса при нажатии кнопки "Старт"
@dp.callback_query_handler(lambda call: call.data == "start")
async def handle_start_query(call: types.CallbackQuery):
    random_image_name = db.get_random_image_name()
    image_info = db.fetch_image_answer(random_image_name)

    if image_info:
        image_path = os.path.join(image_folder, random_image_name)
        with open(image_path, 'rb') as image_file:
            await bot.send_photo(call.message.chat.id, image_file, caption=image_info['description'])

# Функция завершения игры
async def finish_game(message: types.Message):
    global user_score, current_round, user_errors
    await message.answer(f"Игра завершена! Ваш счет: {user_score} из 10. Сейчас покажу, где были ошибки...")

    for image_name, error_message in user_errors:
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    user_score = 0
    current_round = 0
    user_errors = []
    await message.answer("Возвращение в главное меню")

# Запуск бота с использованием асинхронной функции для обработки событий
async def start_bot():
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())