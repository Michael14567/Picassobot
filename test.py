import os
import asyncio
from aiogram import Bot, Dispatcher, types
import sqlite3

# Установка переменной окружения с токеном
os.environ['TG_BOT_TOKEN'] = '6772341949:AAFo-jFQ2xUNGY9dTxtBixsgVckyp4eanJc'

# Получение токена из переменной окружения
API_TOKEN = os.getenv('TG_BOT_TOKEN')

# Инициализация бота и диспетчера с полученным токеном
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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

## Функция для получения информации об изображении
async def fetch_image_answer(image_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT answer, description, error_message FROM image_answers WHERE image_name = ?", (image_name,))
    image_info = cursor.fetchone()
    conn.close()
    
    return image_info

# Обработчик запроса на начало игры
@dp.callback_query_handler(lambda call: call.data == 'start_game')
async def handle_start_query(call: types.CallbackQuery):
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
            await bot.send_photo(call.message.chat.id, image_file, caption=description, reply_markup=inline_kb)
    else:
        await call.message.answer("Извините, произошла ошибка при получении изображения.")

# Добавляем обработчик для выбора режимов игры
@dp.callback_query_handler(lambda call: call.data == 'change_mode')
async def change_mode(call: types.CallbackQuery):
    # Создаем inline-клавиатуру для выбора режима
    inline_kb = types.InlineKeyboardMarkup(row_width=2)
    standard_mode = types.InlineKeyboardButton("Картины Стандарт", callback_data='mode_standard')
    pro_mode = types.InlineKeyboardButton("Картины PRO", callback_data='mode_pro')
    anime_mode = types.InlineKeyboardButton("Anime", callback_data='mode_anime')
    inline_kb.add(standard_mode, pro_mode, anime_mode)

    await call.message.answer("Выберите режим игры:", reply_markup=inline_kb)

# Обработчик для выбора конкретного режима
@dp.callback_query_handler(lambda call: call.data.startswith('mode_'))
async def handle_mode_selection(call: types.CallbackQuery):
    user_id = call.from_user.id
    selected_mode = call.data.split('_')[1]

    # Сохраняем выбранный режим для пользователя
    user_game_data[user_id]['mode'] = selected_mode

    # Можно начать новую игру или что-то в этом роде
    # Например, отправить сообщение о начале нового режима
    await call.message.answer(f"Режим '{selected_mode}' выбран. Начнем игру!")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_image_path = os.path.join(image_folder, 'welcome.jpg')
    with open(welcome_image_path, 'rb') as welcome_image:
        await message.answer_photo(welcome_image)

    welcome_text = (
        "(ﾉ◕ヮ◕)ﾉ Добро пожаловать !  \n"
        "Тебе нужно будет угадать \n"
        "Какая картина написанна художником \n"
        "А какая сгенерирована AI\n"
        "Вперед! открой меню и СТАРТ\n"
        "[Discord](https://discord.gg/GmGfbgWDWk)\n"
        "[Поддержка](https://t.me/Dnec4)\n"
    )

    inline_keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Старт", callback_data='start_game')
    modes_button = types.InlineKeyboardButton("Режимы", callback_data='change_mode')
    settings_button = types.InlineKeyboardButton("Настройки", callback_data='settings')
    inline_keyboard.row(start_button)
    inline_keyboard.row(modes_button, settings_button)

    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=inline_keyboard)

# Словарь для хранения состояния игры пользователей
user_game_data = {}

# Обработчик для выбора ответа пользователем
@dp.callback_query_handler(lambda call: call.data.startswith('real_') or call.data.startswith('generated_'))
async def handle_answer(call: types.CallbackQuery):
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

    # Проверяем, достигли ли мы 10 раундов
    if game_data['round'] >= 10:
        await finish_game(call.message, user_id)
    else:
        # Переходим к следующему раунду
        await send_next_image(call.message, user_id)

# Функция для отправки следующего изображения
async def send_next_image(message, user_id):
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
            await bot.send_photo(message.chat.id, image_file, caption=description, reply_markup=inline_kb)
    else:
        await message.answer("Извините, произошла ошибка при получении изображения.")

# Функция для завершения игры и показа результатов
async def finish_game(message, user_id):
    game_data = user_game_data[user_id]
    score = game_data['score']
    errors = game_data['errors']

    # Отправляем результаты
    await message.answer(f"Игра завершена! Ваш счет: {score} из 10. Ваши ошибки:")

    for image_name, error_message in errors:
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    # Удаляем данные игры для пользователя
    del user_game_data[user_id]

# Глобальный словарь для хранения данных игры пользователей
user_game_data = {}
# Функция для получения случайного аниме-изображения из anime.db
async def get_random_anime_image():
    conn = sqlite3.connect('anime.db')  # Убедитесь, что указали правильный путь к файлу
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_name FROM anime_answers ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

# Функция для получения информации об аниме-изображении
async def fetch_anime_answer(image_name):
    conn = sqlite3.connect('anime.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT answer, description, error_message FROM anime_answers WHERE image_name = ?", (image_name,))
    result = cursor.fetchone()
    conn.close()
    
    return result

# Обработчик текстовых сообщений для режима Anime
@dp.message_handler(lambda message: user_game_data.get(message.from_user.id, {}).get('mode') == 'anime')
async def handle_anime_guess(message: types.Message):
    user_id = message.from_user.id
    game_data = user_game_data.get(user_id, None)

    if game_data and game_data['round'] < 10:
        # Получение данных текущего изображения
        current_image = game_data['current_image']
        correct_answer, _, error_message = await fetch_anime_answer(current_image)

        # Проверка ответа
        if message.text.strip().lower() == correct_answer.lower():
            game_data['score'] += 1
        else:
            game_data['errors'].append((current_image, error_message))

        game_data['round'] += 1

        # Если игра не закончилась, отправляем следующее изображение
        if game_data['round'] < 10:
            await send_next_anime_image(message)
        else:
            await finish_game(message, user_id)
    else:
        await message.answer("Начните новую игру, выбрав режим.")

# Функция для отправки следующего аниме-изображения
async def send_next_anime_image(message):
    user_id = message.from_user.id
    random_image_name = await get_random_anime_image()
    user_game_data[user_id]['current_image'] = random_image_name

    image_path = os.path.join(image_folder, random_image_name)
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(message.chat.id, image_file)

# Модифицируем обработчик выбора режима
@dp.callback_query_handler(lambda call: call.data == 'mode_anime')
async def handle_mode_anime(call: types.CallbackQuery):
    user_id = call.from_user.id

    # Инициализация данных игры для режима Anime
    user_game_data[user_id] = {'mode': 'anime', 'score': 0, 'round': 0, 'errors': [], 'current_image': None}

    await call.message.answer("Режим 'Anime' выбран. Начнем игру!")
    await send_next_anime_image(call.message)
# Функция для отправки следующего аниме-изображения
async def send_next_anime_image(message):
    user_id = message.from_user.id
    random_image_name = await get_random_anime_image()
    user_game_data[user_id]['current_image'] = random_image_name

    image_path = os.path.join(image_folder, random_image_name)
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(message.chat.id, image_file)

# Функция для завершения игры и показа результатов
async def finish_game(message, user_id):
    game_data = user_game_data[user_id]
    score = game_data['score']
    errors = game_data['errors']

    # Отправляем результаты
    await message.answer(f"Игра завершена! Ваш счет: {score} из 10. Ваши ошибки:")

    for image_name, error_message in errors:
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'rb') as image_file:
            await message.answer_photo(image_file, caption=error_message)

    # Удаляем данные игры для пользователя
    del user_game_data[user_id]
# Запуск бота
async def start_bot():
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())