import time
from learnlogic import difference_time


class ControlDB:
    def __init__(self, db):
        self.db = db
        self.curs = self.db.cursor()

    def register_new_client(self, username: str, password: str):
        print("*")
        if username != '' and password != '':
            self.curs.execute(f"""INSERT INTO client (login, password) VALUES (
                       '{username}', '{password}'
                       )""")
            self.db.commit()

    def find_id_client(self, username: str, password=None) -> list or None:

        if password is None:
            self.curs.execute(f"""SELECT id FROM client WHERE login='{username}'""")
        else:
            self.curs.execute(f"""SELECT id FROM client WHERE login='{username}' AND password='{password}'""")

        id_client = self.curs.fetchall()
        if not id_client:
            return None
        else:
            return id_client[0][0]

    def authorization(self, username: str, password: str) -> bool:
        if self.find_id_client(username, password) is None:
            print("Не допущен")
            return False
        else:
            print("Успешная авторизация")
            return True

    def count_l_words(self, id_client: int) -> int:
        """
        Підраховує кількість вивчених слів
        """
        self.curs.execute(f"""
        SELECT count(id_word) FROM learned_words WHERE id_client={id_client} AND Id_lerned>2;
        """)
        amount = self.curs.fetchall()[0][0]
        if amount:
            return amount
        else:
            return 0

    def transfer_5_words(self, id_client: int):
        """
        Додае до таблиці вивчених слів нові 5 слів
        """
        id_las_word = self.__get_idlast_word(id_client)

        if id_las_word is None:
            id_las_word = 0
        start_time = time.time()
        self.curs.execute(f"""
           INSERT INTO learned_words (id_client, id_word, id_lerned, start_time) VALUES 
           ({id_client}, {id_las_word+1}, 1,{start_time}),
           ({id_client}, {id_las_word+2}, 1,{start_time}),
           ({id_client}, {id_las_word+3}, 1,{start_time}),
           ({id_client}, {id_las_word+4}, 1,{start_time}),
           ({id_client}, {id_las_word+5}, 1,{start_time})
            """)
        self.db.commit()

    def __get_idlast_word(self, id_client: int) -> int:
        """
        Повертає id останнього вивченого слова
        """
        self.curs.execute(f"""SELECT max(id_word) FROM learned_words WHERE id_client={id_client}""")
        id_word = self.curs.fetchall()[0][0]
        return id_word

    def __get_learned_words(self, id_client: int) -> list:
        """
        Повертає список вивчених слів
        """
        self.curs.execute(f"""SELECT * FROM learned_words WHERE id_client={id_client}""")
        ls = self.curs.fetchall()
        return ls

    def __get_status_dict(self) -> dict:
        """
        Повертає словарь
        ключ - ід статуса
        значенна - час до наступного повторення
        """
        self.curs.execute(f"""SELECT * FROM status_learning""")
        st_learning = {}
        for i in self.curs.fetchall():
            st_learning[i[0]] = i[1]

        return st_learning

    def check_repead_words(self, id_client: int) -> list:
        """
        Повертає список слів які потрібно повторити
        """
        repead_words = []
        learned_words = self.__get_learned_words(id_client)
        st_learning = self.__get_status_dict()

        if not learned_words:
            return repead_words
        else:
            for i in learned_words:
                if difference_time(i[3], st_learning.get(i[2])) >= 0:
                    repead_words.append(i)

        return repead_words

    def zeroing_status(self, id_client: int, id_words: int):
        """
        Обнуляє статус вивчення переданого слова в заданого клієнта
        """
        self.curs.execute(f"""
        UPDATE learned_words SET id_lerned=1, start_time={time.time()}
         WHERE id_client={id_client} AND id_word={id_words}""")
        self.db.commit()

    def lifting_status(self, id_client, id_words):
        """
        Піднімає статус вивченого слова на +1 в заданого клієнта
        """
        self.curs.execute(f"""
        UPDATE learned_words SET id_lerned=id_lerned+1, start_time={time.time()}
         WHERE id_client={id_client} AND id_word={id_words}""")
        self.db.commit()

    def get_date_word(self, id_word: int):
        """
        Повертає всю інформацію про задане слово
        """
        self.curs.execute(f"""SELECT * FROM words WHERE id={id_word}""")

        return self.curs.fetchall()[0]


