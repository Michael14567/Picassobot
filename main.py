import asyncio
from aiogram import Bot, Dispatcher, types
import os

# Импортируем функции из других модулей
from paintings_mode import handle_start_query, send_next_image, finish_game, handle_answer
from anime_mode import handle_anime_guess, send_next_anime_image, handle_mode_anime

# Установка переменной окружения с токеном
os.environ['TG_BOT_TOKEN'] = '6772341949:AAFo-jFQ2xUNGY9dTxtBixsgVckyp4eanJc'

# Получение токена из переменной окружения
API_TOKEN = os.getenv('TG_BOT_TOKEN')

# Инициализация бота и диспетчера с полученным токеном
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

image_folder = 'C:/Users/spiri/Desktop/bot'
# Словарь для хранения состояния игры пользователей
user_game_data = {}

# Обработчик для выбора "Реальная" или "Сгенерированная"
@dp.callback_query_handler(lambda call: call.data.startswith('real_') or call.data.startswith('generated_'))
async def handle_real_or_generated(call: types.CallbackQuery):
    await handle_answer(call, user_game_data)

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


# Обработчик для выбора режимов игры
@dp.callback_query_handler(lambda call: call.data == 'change_mode')
async def change_mode(call: types.CallbackQuery):
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

    # Инициализация или обновление данных игры для пользователя
    user_game_data[user_id] = {'mode': selected_mode, 'score': 0, 'round': 0, 'errors': []}

    if selected_mode == 'anime':
        await send_next_anime_image(call.message, user_game_data)
    else:
        await handle_start_query(call, user_game_data)


    # Сохраняем выбранный режим для пользователя
    user_game_data[user_id] = {'mode': selected_mode, 'score': 0, 'round': 0, 'errors': [], 'current_image': None}

    if selected_mode == 'anime':
        await send_next_anime_image(call.message, user_game_data)
    else:
        await handle_start_query(call, user_game_data)

# Обработчик текстовых сообщений для режима Anime
@dp.message_handler(lambda message: user_game_data.get(message.from_user.id, {}).get('mode') == 'anime')
async def handle_anime_text(message: types.Message):
    await handle_anime_guess(message, user_game_data)

# Запуск бота
async def start_bot():
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
