import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
import sqlite3

# Initialize bot and dispatcher
API_TOKEN = '6772341949:AAFo-jFQ2xUNGY9dTxtBixsgVckyp4eanJc'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

image_folder = 'C:/Users/spiri/Desktop/bot'
# Set up database connection
DB_FILE = 'Картины.db'

# Function to fetch a random image name from the database
async def get_random_image_name():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_name FROM image_answers ORDER BY RANDOM() LIMIT 1")
    random_image_name = cursor.fetchone()[0]  # Fetch the first column value from the result
    conn.close()
    
    return random_image_name

# Function to fetch image details from the database based on its name
async def fetch_image_answer(image_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT answer, description, error_message FROM image_answers WHERE image_name = ?", (image_name,))
    image_info = cursor.fetchone()  # Fetch the row of information
    conn.close()
    
    if image_info:
        return {
            'answer': image_info[0],
            'description': image_info[1],
            'error_message': image_info[2]
        }
    else:
        return None

#@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Welcome image
    welcome_image_path = os.path.join(image_folder, 'welcome.jpg')

    # Sending the welcome image
    with open(welcome_image_path, 'rb') as welcome_image:
        await message.answer_photo(welcome_image)

    # Welcome text
    welcome_text = (
        "(ﾉ◕ヮ◕)ﾉ Добро пожаловать !  \n"
        "Тебе нужно будет угадать \n"
        "Какая картина написанна художником \n"
        "А какая сгенерирована AI\n"
        "Вперед! открой меню и СТАРТ\n"
        "[Discord](https://discord.gg/GmGfbgWDWk)\n"
        "[Поддержка](https://t.me/Dnec4)\n"
    )

    # Inline keyboard with menu buttons
    inline_keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Старт", callback_data='start_game')
    modes_button = types.InlineKeyboardButton("Режимы", callback_data='modes')
    settings_button = types.InlineKeyboardButton("Настройки", callback_data='settings')
    inline_keyboard.row(start_button)
    inline_keyboard.row(modes_button, settings_button)

    # Sending the welcome text with the inline keyboard
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=inline_keyboard)
# Handle callback query for starting the game
@dp.callback_query_handler(lambda call: call.data == 'start_game')
async def handle_start_query(call: types.CallbackQuery):
    random_image_name = await get_random_image_name()
    image_info = await fetch_image_answer(random_image_name)

    if image_info:
        image_path = os.path.join(image_folder, random_image_name)
        with open(image_path, 'rb') as image_file:
            await bot.send_photo(call.message.chat.id, image_file, caption=image_info['description'])
async def finish_game(message: types.Message):
    global user_score, current_round, user_errors

    # Display user's score
    await message.answer(f"Игра завершена! Ваш счет: {user_score} из 10. Сейчас покажу, где были ошибки...")

    # Display errors from previous rounds
    for image_name, error_message in user_errors:
        # Display the error images and messages
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    # Reset game parameters for a new game
    user_score = 0
    current_round = 0
    user_errors = []
    await message.answer("Возвращение в главное меню")


# Функция завершения игры
async def finish_game(message: types.Message):
    global user_score, current_round, user_errors

    # Display user's score
    await message.answer(f"Игра завершена! Ваш счет: {user_score} из 10. Сейчас покажу, где были ошибки...")

    # Display errors from previous rounds
    for image_name, error_message in user_errors:
        # Display the error images and messages
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    # Reset game parameters for a new game
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

    