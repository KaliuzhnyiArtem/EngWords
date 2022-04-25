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

    def authorization(self, username, password):
        self.curs.execute(f"""SELECT id FROM client WHERE login='{username}' AND password='{password}'""")

        if not self.curs.fetchall():
            print("Не допущен")
            return False
        else:
            print("Успешная авторизация")
            return True

    def check_username(self, username):
        self.curs.execute(f"""SELECT * FROM client WHERE login='{username}'""")

        if self.curs.fetchall():
            return False
        else:
            return True




