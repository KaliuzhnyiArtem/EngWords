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
        username = request.form['username']
        password = request.form['password']

        # Создание новго аканта
        if 'create_account' in request.form:
            cont_db = ControlDB(get_db())
            if cont_db.find_id_client(username) is None:
                cont_db.register_new_client(username, password)

        # Вход в профиль
        elif 'enter' in request.form:
            cont_db = ControlDB(get_db())
            access = cont_db.authorization(username, password)
            if access:
                session['id_client'] = cont_db.find_id_client(username, password)
                session['username'] = username
                session['password'] = password
                return redirect(url_for('info_page', username=username))

    return render_template('index.html')


@app.route("/infopage/<username>", methods=["POST", "GET"])
def info_page(username):

    if request.method == "POST":
        return 'test'

    cont_db = ControlDB(get_db())
    if session['id_client'] == cont_db.find_id_client(username):
        return render_template('infopage.html', count_l_words=cont_db.count_l_words(session['id_client']))
    else:
        return redirect(url_for('index'))


@app.route('/learnpage')
def learn_words():
    return render_template('learnpage.html')


if __name__ == "__main__":
    app.run(debug=True)
