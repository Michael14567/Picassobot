import sqlite3
import json
import random

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
