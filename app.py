from flask import Flask, render_template, redirect, url_for, g, request, abort
import sqlite3

app = Flask(__name__)

isAdmin = False

DATABASE = 'sota.db'

type_paper = "paper"
type_author = "author"
type_topic = "topic"

option_add = "add"
option_update = "update"
option_delete = "delete"


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form["author_name"]
        surname = request.form["author_surname"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO authors (author_name, author_surname) VALUES(?, ?)""", (name, surname))
        connection.commit()
        connection.close()

        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        connection = sqlite3.connect('sota.db')
        for row in cursor.execute("""SELECT * FROM authors"""):
            print(row)
        connection.close()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("add_author.html")
    else:
        return abort(404)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if type_paper in request.form:
            selected_option = request.form[type_paper]
            if selected_option == option_add:
                return selected_option + type_paper
            elif selected_option == option_update:
                return selected_option + type_paper
            elif selected_option == option_delete:
                return selected_option + type_paper
            else:
                return abort(404)
        elif type_author in request.form:
            selected_option = request.form[type_author]
            if selected_option == option_add:
                return redirect(url_for('add_author'))
            elif selected_option == option_update:
                return selected_option + type_author
            elif selected_option == option_delete:
                return selected_option + type_author
            else:
                return abort(404)
        elif type_topic in request.form:
            selected_option = request.form[type_topic]
            if selected_option == option_add:
                return selected_option + type_topic
            elif selected_option == option_update:
                return selected_option + type_topic
            elif selected_option == option_delete:
                return selected_option + type_topic
            else:
                return abort(404)
        else:
            return abort(404)
    elif request.method == 'GET':
        if isAdmin:
            return render_template("index_admin.html")
        else:
            return render_template("index_user.html")
    else:
        return abort(404)


@app.route('/login', )
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


def set_admin(true_or_false):
    global isAdmin
    isAdmin = true_or_false


@app.route("/as_admin/", methods=['POST'])
def as_admin():
    set_admin(True)
    return redirect(url_for('index'))


@app.route("/as_user/", methods=['POST'])
def as_user():
    set_admin(False)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
