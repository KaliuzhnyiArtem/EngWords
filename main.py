from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3
import os
from controlDB import ControlDB
import random as r


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


def save_in_session(engword, rusword, trans, id_word, status_learn):
    session['engword'] = engword
    session['rusword'] = rusword
    session['trans'] = trans
    session['id_word'] = id_word
    session['status_learn'] = status_learn


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Створення ного акаунта
        if 'create_account' in request.form:
            cont_db = ControlDB(get_db())
            if cont_db.find_id_client(username) is None:
                cont_db.register_new_client(username, password)

        # Вхід в профіль
        elif 'enter' in request.form:
            cont_db = ControlDB(get_db())
            access = cont_db.authorization(username, password)
            if access:
                session['username'] = username
                session['password'] = password
                session['id_client'] = cont_db.find_id_client(username, password)
                return redirect(url_for('info_page', username=username))

    return render_template('index.html')


@app.route('/learnpage/answer/<username>', methods=["POST", "GET"])
def learn_answer(username):

    cont_db = ControlDB(get_db())
    if session['id_client'] == cont_db.find_id_client(username):
        if request.method == 'POST':

            if 'repeat' in request.form:
                cont_db.zeroing_status(session['id_client'], session['id_word'])
                return redirect(url_for('learn_words', username=username))

            elif 'know' in request.form:
                if session['status_learn'] == 0:
                    cont_db.lifting_status(session['id_client'], session['id_word'], step=2)
                else:
                    cont_db.lifting_status(session['id_client'], session['id_word'])
                return redirect(url_for('learn_words', username=username))

        if session['status_learn'] == 2:
            return render_template('learn_answer.html', engword=session['rusword'],
                                   trans=session['engword'], rus=session['trans'])
        else:
            return render_template('learn_answer.html', engword=session['engword'],
                                   trans=session['trans'], rus=session['rusword'])
    else:
        return redirect(url_for('index'))


@app.route('/learnpage/<username>', methods=["POST", "GET"])
def learn_words(username):
    cont_db = ControlDB(get_db())

    # Перевірка доступу до данного url
    if session['id_client'] == cont_db.find_id_client(username):
        repead_words: list = cont_db.check_repead_words(session['id_client'])

        if not repead_words:
            return redirect(url_for('info_page', username=username))

        else:
            if request.method == 'POST':
                if 'show_answer' in request.form:
                    return redirect(url_for('learn_answer', username=username))

            studying_word: tuple = cont_db.get_date_word(repead_words[0][1])

            save_in_session(studying_word[1], studying_word[2],
                            studying_word[3], studying_word[0], repead_words[0][2])

            if session['status_learn'] == 2:
                return render_template('learnpage.html', engword=studying_word[2])
            else:
                return render_template('learnpage.html', engword=studying_word[1],
                                       trans=studying_word[3])
    else:
        return redirect(url_for('index'))


@app.route("/infopage/<username>", methods=["GET", "POST"])
def info_page(username):
    cont_db = ControlDB(get_db())

    if request.method == "POST":
        # Активація клавіші "Вчити нові слова"
        if 'learb' in request.form:
            cont_db.transfer_5_words(session['id_client'])
            return redirect(url_for('learn_words', username=username))
        elif 'repetitionWords' in request.form:
            return redirect(url_for('learn_words', username=username))

    # Перевірка доступу до данного url
    if session['id_client'] == cont_db.find_id_client(username):
        return render_template('infopage.html',
                               count_l_words=cont_db.count_l_words(session['id_client']),
                               count_repeat=len(cont_db.check_repead_words(session['id_client'])),
                               repeat_words=cont_db.check_repead_words(session['id_client']))
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
