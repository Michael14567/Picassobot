import os
import sqlite3
from aiogram import types

# Путь к папке с изображениями
image_folder = 'C:/Users/spiri/Desktop/bot'
DB_FILE = 'Картины.db'

# Функция для получения случайного имени изображения
async def get_random_image_name():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_name FROM image_answers ORDER BY RANDOM() LIMIT 1")
    random_image_name = cursor.fetchone()[0]
    conn.close()
    
    return random_image_name

# Функция для получения информации об изображении
async def fetch_image_answer(image_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT answer, description, error_message FROM image_answers WHERE image_name = ?", (image_name,))
    image_info = cursor.fetchone()
    conn.close()
    
    return image_info

# Обработчик запроса на начало игры
async def handle_start_query(call: types.CallbackQuery, user_game_data):
    random_image_name = await get_random_image_name()
    image_info = await fetch_image_answer(random_image_name)

    if image_info:
        description = image_info[1]  # Описание изображения
        image_path = os.path.join(image_folder, random_image_name)

        # Создаем inline-клавиатуру
        inline_kb = types.InlineKeyboardMarkup(row_width=2)
        real_button = types.InlineKeyboardButton("Реальная", callback_data=f"real_{random_image_name}")
        generated_button = types.InlineKeyboardButton("Сгенерированная", callback_data=f"generated_{random_image_name}")
        inline_kb.add(real_button, generated_button)

        with open(image_path, 'rb') as image_file:
            await call.message.bot.send_photo(call.message.chat.id, image_file, caption=description, reply_markup=inline_kb)
    else:
        await call.message.answer("Извините, произошла ошибка при получении изображения.")

# Функция для отправки следующего изображения
async def send_next_image(message, user_game_data):
    random_image_name = await get_random_image_name()
    image_info = await fetch_image_answer(random_image_name)

    if image_info:
        description = image_info[1]
        image_path = os.path.join(image_folder, random_image_name)

        # Создаем inline-клавиатуру
        inline_kb = types.InlineKeyboardMarkup(row_width=2)
        real_button = types.InlineKeyboardButton("Реальная", callback_data=f"real_{random_image_name}")
        generated_button = types.InlineKeyboardButton("Сгенерированная", callback_data=f"generated_{random_image_name}")
        inline_kb.add(real_button, generated_button)

        with open(image_path, 'rb') as image_file:
            await message.bot.send_photo(message.chat.id, image_file, caption=description, reply_markup=inline_kb)
    else:
        await message.answer("Извините, произошла ошибка при получении изображения.")

# Обработчик для выбора ответа пользователем
async def handle_answer(call: types.CallbackQuery, user_game_data):
    user_id = call.from_user.id
    answer, image_name = call.data.split('_')
    correct_answer, _, error_message = await fetch_image_answer(image_name)

    # Инициализация данных игры, если они еще не существуют для пользователя
    if user_id not in user_game_data:
        user_game_data[user_id] = {'score': 0, 'round': 0, 'errors': []}

    game_data = user_game_data[user_id]

    # Проверка ответа и обновление счета
    if (answer == 'real' and correct_answer == 'Реальная') or (answer == 'generated' and correct_answer == 'Сгенирированная'):
        game_data['score'] += 1
    else:
        game_data['errors'].append((image_name, error_message))

    game_data['round'] += 1
    if game_data['round'] >= 10:
        await finish_game(call.message, user_game_data)
    else:
        await send_next_image(call.message, user_game_data)

# Функция для завершения игры и показа результатов
async def finish_game(message: types.Message, user_game_data):
    user_id = message.from_user.id

    # Убедитесь, что данные для пользователя существуют
    if user_id not in user_game_data:
        await message.answer("Произошла ошибка: данные игры не найдены.")
        return

    game_data = user_game_data[user_id]
    game_data = user_game_data[user_id]
    score = game_data['score']
    errors = game_data['errors']

    await message.answer(f"Игра завершена! Ваш счет: {score} из 10. Ваши ошибки:")

    for image_name, error_message in errors:
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    # Удаляем данные игры для пользователя
    del user_game_data[user_id]
