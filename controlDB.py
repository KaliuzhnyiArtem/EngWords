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




