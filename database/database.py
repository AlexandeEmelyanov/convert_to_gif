import os
import sqlite3

def create_database():# Настройка базы данных SQLite для хранения пользователей
    if not os.path.exists("./database/database.db"):
        conn = sqlite3.connect("./database/database.db")
        cursor = conn.cursor()
        # Создаём таблицу, если её ещё нет
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, username VARCHAR(100));")
        conn.commit()
        conn.close()


def insert_database(user_id, username):
    conn = sqlite3.connect("./database/database.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",(user_id, username))
    conn.commit()
    conn.close()