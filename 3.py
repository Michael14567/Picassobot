import sqlite3

DB_FILE = 'anime.db'
image_answers = {
    '1000.jpg': {'answer': 'Атака Титанов', 'description': 'Леви Аккерман', 'error_message': 'Одно из самых запоминаюшихся аниме'},
    '1001.jpg': {'answer': 'Атака Титанов', 'description': 'Микасса Аккерман', 'error_message': 'Один из самых интересеных персонажей интересного аниме'},
    '1002.jpg': {'answer': 'Атака Титанов', 'description': 'Ханджи Зое', 'error_message': 'Разведкорпус отдал сердца'},
    '1003.jpg': {'answer': 'Атака Титанов', 'description': 'Армин Арлерт', 'error_message': 'Прикольный персонаж'},
    '1004.jpg': {'answer': 'Берсерк', 'description': 'Гатц', 'error_message': 'Первое мое анимэ) Не могу оценивать'},
    '1005.jpg': {'answer': 'Берсерк', 'description': 'Гриффит', 'error_message': 'Вот что значит идти к цели несмотря ниначто'},
    '1006.jpg': {'answer': 'Берсерк', 'description': 'Каска', 'error_message': 'Просто запоминающийся персонаж из хорошего аниме'},
    '1007.jpg': {'answer': 'Акира', 'description': 'Сётаро Канэда', 'error_message': 'Классика'},
    '1008.jpeg': {'answer': 'Призрак в доспехах', 'description': 'Мотоко Кусанаги', 'error_message': 'Chatgpt оценил'},
    '1009.jpg': {'answer': 'Скитальцы', 'description': ' Тоёхиса Симадзу', 'error_message': 'Аниме где армия гитлера хочет уничтожить мир , но им противостоят японские мастера меча и один ебанутый чел с вертолетом'},
    '1010.jpeg': {'answer': 'Твое имя', 'description': 'Мицуха', 'error_message': 'Что сказать , сказка.)'},
    '1011.jpg': {'answer': 'Дитя Погоды', 'description': 'Ходака Морисима', 'error_message': 'Смотрел давно , но зашло'},
    '1012.jpeg': {'answer': 'Форма Голоса', 'description': 'Сёя Исида и  Сёко Нисимия', 'error_message': 'Незнаю , на любителя .'},
    '1013.jpg': {'answer': 'Убийца Акаме', 'description': 'Акаме', 'error_message': '---'},
    '1014.jpg': {'answer': 'Коносуба', 'description': 'Пиво пиво', 'error_message': 'Неплохой тайтл для нормисов'},
    '1015.jpg': {'answer': 'Клинок рассекающий демонов', 'description': 'Кабанчик', 'error_message': 'Тайтл для нормисов'},
    '1016.jpg': {'answer': 'Сага о Винланде', 'description': 'Торфин', 'error_message': 'Развитие персонажа поразительное. самое христианское аниме'},
    '1017.jpg': {'answer': 'Сага о Винланде', 'description': 'Аскелад', 'error_message': 'У тебя нет врагов ?'},
    '1018.png': {'answer': 'Боец Баки', 'description': 'Баки', 'error_message': 'Под это только качаться'},
    '1019.jpg': {'answer': 'Дорохедоро', 'description': '---', 'error_message': 'top'},
    '1020.jpeg': {'answer': 'Стальной Алхимик', 'description': 'Эдвард Элрик', 'error_message': 'Философское аниме'},
    '1021.jpg': {'answer': 'Доктор Стоун', 'description': 'Стоун с компанией', 'error_message': 'Аниме смотрел очень давно , зашло , но не досмотрел'},
    '1022.jpg': {'answer': 'Доктор Стоун', 'description': 'Красивые звезды и Камень', 'error_message': 'Аниме смотрел очень давно , зашло , но не досмотрел'},
    '1023.jpg': {'answer': 'Ганрейв', 'description': 'Гарри Макдауэлл', 'error_message': 'приключения и мистика'},
    '1024.jpg': {'answer': 'Магистр дьявольского культа', 'description': 'Лань Ванцзи', 'error_message': 'Можно посмотреть хотябы ради задников'},
    '1025.jpeg': {'answer': 'Ковбой Бибоп', 'description': 'Спайк Шпигель', 'error_message': 'Как будто слушаешь джаз'},
}


# Подключение к базе данных и создание таблицы
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_answers (
        image_name TEXT PRIMARY KEY,
        answer TEXT,
        description TEXT,
        error_message TEXT
    )
''')

# Вставка данных в таблицу
for image_name, info in image_answers.items():
    cursor.execute('''
        INSERT OR REPLACE INTO anime_answers (image_name, answer, description, error_message)
        VALUES (?, ?, ?, ?)
    ''', (image_name, info['answer'], info['description'], info['error_message']))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()

print("Данные успешно добавлены в базу данных.")