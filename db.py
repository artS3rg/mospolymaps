import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, login):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`, `login`) VALUES (?, ?)", (user_id, login))
        return self.conn.commit()

    def add_idea(self, user_id, login, text):
        """Добавляем новую идею в базу"""
        self.cursor.execute("INSERT INTO `ideas` (`user_id`, `login`, `idea`, `status`) VALUES (?, ?, ?, ?)", (user_id, login, text, 'wait'))
        return self.conn.commit()

    def get_sections(self):
        """Получаем список всех разделов"""
        result = list(map(lambda x: x[0], self.cursor.execute("SELECT `name` FROM `sections`").fetchall()))
        return result

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()