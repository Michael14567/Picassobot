import os
import sqlite3
from aiogram import types

# Путь к папке с изображениями аниме
image_folder = 'C:/Users/spiri/Desktop/bot'
ANIME_DB_FILE = 'anime.db'

# Функция для получения случайного аниме-изображения из anime.db
async def get_random_anime_image():
    conn = sqlite3.connect(ANIME_DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_name FROM anime_answers ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

async def handle_mode_anime(call: types.CallbackQuery, user_game_data):
    user_id = call.from_user.id
    user_game_data[user_id] = {'mode': 'anime', 'score': 0, 'round': 0, 'errors': [], 'current_image': None}

    await call.message.answer("Режим 'Anime' выбран. Начнем игру!")
    await send_next_anime_image(call.message, user_game_data)
    
# Функция для получения информации об аниме-изображении
async def fetch_anime_answer(image_name):
    conn = sqlite3.connect(ANIME_DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT answer, description, error_message FROM anime_answers WHERE image_name = ?", (image_name,))
    result = cursor.fetchone()
    conn.close()
    
    return result

# Обработчик текстовых сообщений для режима Anime
async def handle_anime_guess(message: types.Message, user_game_data):
    user_id = message.from_user.id
    game_data = user_game_data.get(user_id, None)

    if game_data and game_data['round'] < 10:
        current_image = game_data['current_image']
        correct_answer, _, error_message = await fetch_anime_answer(current_image)

        if message.text.strip().lower() == correct_answer.lower():
            game_data['score'] += 1
        else:
            game_data['errors'].append((current_image, error_message))

        game_data['round'] += 1

        if game_data['round'] < 10:
            await send_next_anime_image(message, user_game_data)
        else:
            await finish_game(message, user_game_data)
    else:
        await message.answer("Начните новую игру, выбрав режим.")

# Функция для отправки следующего аниме-изображения
async def send_next_anime_image(message: types.Message, user_game_data):
    user_id = message.from_user.id
    random_image_name = await get_random_anime_image()
    user_game_data[user_id]['current_image'] = random_image_name

    image_path = os.path.join(image_folder, random_image_name)
    with open(image_path, 'rb') as image_file:
        await message.bot.send_photo(message.chat.id, image_file)

# Функция для завершения игры и показа результатов
async def finish_game(message: types.Message, user_game_data):
    user_id = message.from_user.id
    game_data = user_game_data[user_id]
    score = game_data['score']
    errors = game_data['errors']

    await message.answer(f"Игра завершена! Ваш счет: {score} из 10. Ваши ошибки:")

    for image_name, error_message in errors:
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    del user_game_data[user_id]
