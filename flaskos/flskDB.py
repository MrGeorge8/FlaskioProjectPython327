import sqlite3
import time
import math
import re
from flask import url_for

class FlaskoDB:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mainmenu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res if res else []
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
            return []

    def add_post(self, title, text, url):
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM post WHERE url LIKE ?",(url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            base = url_for('static', filename="images")
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>", r"\g<tag>" + base + r"/\g<url>>", text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO post VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False
        return True

    def delete_post(self, post_id):
        try:
            self.__cur.execute("DELETE FROM post WHERE id=?", (post_id,))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления статьи из БД" + str(e))
            return False
        return True

    def get_post(self, alias):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM post WHERE url LIKE '{alias}'")
            res = self.__cur.fetchone()
            if res:
                post_data = {
                    'id': res['id'],
                    'title': res['title'],
                    'text': res['text']
                }
                return post_data
            else:
                print(f"No data found for alias '{alias}'")  # Добавьте это для отладки
                return None
        except sqlite3.Error as e:
            print("Ошибка запроса в БД: " + str(e))

        return None

    def get_posts_anonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM post ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))

        return []