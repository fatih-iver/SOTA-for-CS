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


def print_authors():
    connection = sqlite3.connect('sota.db')
    cursor = connection.cursor()
    for author in cursor.execute("""SELECT * FROM authors"""):
        print(author)
    connection.close()


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
        print_authors()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("add_author.html")
    else:
        return abort(404)


@app.route('/update_author', methods=['GET', 'POST'])
def update_author():
    if request.method == 'POST':
        old_author_name = request.form["old_author_name"]
        old_author_surname = request.form["old_author_surname"]
        new_author_name = request.form["new_author_name"]
        new_author_surname = request.form["new_author_surname"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE authors SET author_name=?, author_surname=? WHERE author_name=? and author_surname=?""",
            (new_author_name, new_author_surname, old_author_name, old_author_surname))
        connection.commit()
        connection.close()
        print_authors()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("update_author.html")
    else:
        return abort(404)


@app.route('/delete_author', methods=['GET', 'POST'])
def delete_author():
    if request.method == 'POST':
        author_name = request.form["author_name"]
        author_surname = request.form["author_surname"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute(
            """DELETE FROM authors WHERE author_name=? AND author_surname=?""", (author_name, author_surname))
        connection.commit()
        connection.close()
        print_authors()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("delete_author.html")
    else:
        return abort(404)


def print_topics():
    connection = sqlite3.connect('sota.db')
    cursor = connection.cursor()
    for author in cursor.execute("""SELECT * FROM topics"""):
        print(author)
    connection.close()


@app.route('/add_topic', methods=['GET', 'POST'])
def add_topic():
    if request.method == 'POST':
        topic_name = request.form["topic_name"]
        sota_result = int(request.form["sota_result"])
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO topics (topic_name, sota_result) VALUES(?, ?)""", (topic_name, sota_result))
        connection.commit()
        connection.close()
        print_topics()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("add_topic.html")
    else:
        return abort(404)


@app.route('/update_topic', methods=['GET', 'POST'])
def update_topic():
    if request.method == 'POST':
        old_topic_name = request.form["old_topic_name"]
        old_sota_result = int(request.form["old_sota_result"])
        new_topic_name = request.form["new_topic_name"]
        new_sota_result = int(request.form["new_sota_result"])
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE topics SET topic_name=?, sota_result=? WHERE topic_name=? OR sota_result=?""",
            (new_topic_name, new_sota_result, old_topic_name, old_sota_result))
        connection.commit()
        connection.close()
        print_topics()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("update_topic.html")
    else:
        return abort(404)


@app.route('/delete_topic', methods=['GET', 'POST'])
def delete_topic():
    if request.method == 'POST':
        topic_name = request.form["topic_name"]
        sota_result = int(request.form["sota_result"])
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute(
            """DELETE FROM topics WHERE topic_name=? OR sota_result=?""", (topic_name, sota_result))
        connection.commit()
        connection.close()
        print_topics()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("delete_topic.html")
    else:
        return abort(404)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "author" in request.form:
            selected_option = request.form["author"]
            if selected_option == option_add:
                return redirect(url_for('add_author'))
            elif selected_option == option_update:
                return redirect(url_for('update_author'))
            elif selected_option == option_delete:
                return redirect(url_for('delete_author'))
            else:
                return abort(404)
        elif "topic" in request.form:
            selected_option = request.form["topic"]
            if selected_option == option_add:
                return redirect(url_for('add_topic'))
            elif selected_option == option_update:
                return redirect(url_for('update_topic'))
            elif selected_option == option_delete:
                return redirect(url_for('delete_topic'))
            else:
                return abort(404)
        elif "paper" in request.form:
            selected_option = request.form["paper"]
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
