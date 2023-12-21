import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def get_user_stud(self, user_id):
        """Достаем stud_status юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[-1]

    def add_user(self, user_id, login, status):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users (user_id, login, stud_status) VALUES (?, ?, ?)",
                            (user_id, login, status))
        return self.conn.commit()

    def add_idea(self, user_id, login, text):
        """Добавляем новую идею в базу"""
        self.cursor.execute("INSERT INTO ideas (user_id, login, idea, status) VALUES (?, ?, ?, ?)",
                            (user_id, login, text, 'wait'))
        return self.conn.commit()

    def get_sections(self):
        """Получаем список всех разделов студентов"""
        result = list(map(lambda x: x[0], self.cursor.execute("SELECT name FROM sections").fetchall()))[1:]
        return result

    def get_employee_sections(self):
        """Получаем список всех разделов работников"""
        result = list(map(lambda x: x[0], self.cursor.execute("SELECT name FROM employee_sections").fetchall()))[1:]
        return result

    def get_answers(self, section_name):
        """Получаем список ответов и их id из определённого раздела"""
        result = list(
            self.cursor.execute("SELECT id, text FROM information WHERE section=(SELECT id FROM sections "
                                "WHERE name = ?)", (section_name,)).fetchall())
        result.sort(key=lambda x: x[1])
        return result

    def get_staff_answers(self, section_name):
        """Получаем список ответов и их id из определённого раздела"""
        result = list(
            self.cursor.execute("SELECT id, text FROM employee_info WHERE section=(SELECT id FROM employee_sections "
                                "WHERE name = ?)", (section_name,)).fetchall())
        result.sort(key=lambda x: x[1])
        return result

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
