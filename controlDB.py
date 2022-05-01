import time
class ControlDB:
    def __init__(self, db):
        self.db = db

        self.curs = self.db.cursor()

    def register_new_client(self, username, password):
        print("*")
        if username != '' and password != '':
            self.curs.execute(f"""INSERT INTO client (login, password) VALUES (
                       '{username}', '{password}'
                       )""")
            self.db.commit()

    def find_id_client(self, username, password=None):

        if password is None:
            self.curs.execute(f"""SELECT id FROM client WHERE login='{username}'""")
        else:
            self.curs.execute(f"""SELECT id FROM client WHERE login='{username}' AND password='{password}'""")

        id_client = self.curs.fetchall()
        if not id_client:
            return None
        else:
            return id_client[0][0]

    def authorization(self, username, password):
        if self.find_id_client(username, password) is None:
            print("Не допущен")
            return False
        else:
            print("Успешная авторизация")
            return True

    def count_l_words(self, id_client):
        self.curs.execute(f"""
        SELECT count(id_word) FROM learned_words WHERE id_client={id_client} AND Id_lerned>2;
        """)
        amount = self.curs.fetchall()[0][0]
        if amount:
            return amount
        else:
            return 0

    def transfer_5_words(self, id_client, id_las_word):
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

    def get_idlast_word(self, id_client=1):
        self.curs.execute(f"""SELECT max(id_word) FROM learned_words WHERE id_client=1""")
        id_word = self.curs.fetchall()[0][0]
        return id_word

    #Dont used
    def get_learned_words(self, id_client):
        self.curs.execute(f"""SELECT * FROM learned_words WHERE id_client={id_client}""")
        return self.curs.fetchall()

    def find_words_repetition(self, id_client):
        time_now = time.time()
        self.curs.execute(f"""
        SELECT * FROM learned_words AS lw WHERE id_client={id_client} AND {time_now}-lw.start_time
        """)
        
        
    def check_learned_words(self):
        # Проверка на время
        # Плучить все выученые слова клиента
        pass
