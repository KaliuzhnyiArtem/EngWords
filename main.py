from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3
import os
from controlDB import ControlDB


# Конфигурация
DATABASE = '/tmp/engwords.db'
DEBUG = True
SECRET_KEY = 'aafsehf73f3hafh23fhajdfh23f82fsdkhf2'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'engwords.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":

        # Создание новго аканта
        if 'create_account' in request.form:
            cont_db = ControlDB(get_db())
            if cont_db.check_username(request.form['username']):
                cont_db.register_new_client(request.form['username'], request.form['password'])
                print('create acount')

        # Вход в профиль
        elif 'enter' in request.form:
            cont_db = ControlDB(get_db())
            access = cont_db.authorization(request.form['username'], request.form['password'])
            if access:
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                print('enter')
                return redirect(url_for('info_page', username=request.form['username']),)

    return render_template('index.html')


@app.route("/infopage/<username>")
def info_page(username):
    return render_template('infopage.html')


if __name__ == "__main__":
    app.run(debug=True)
