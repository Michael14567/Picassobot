import sqlite3

DB_FILE = 'Картины.db'  # Убедитесь, что путь к вашей базе данных указан правильно

def check_images_in_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT image_name FROM image_answers")
        images = cursor.fetchall()
        if images:
            print("Список изображений в базе данных:")
            for image in images:
                print(image[0])
        else:
            print("В базе данных нет изображений.")
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_images_in_database()