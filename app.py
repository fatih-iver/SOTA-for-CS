from flask import Flask, render_template, redirect, url_for, g, request, abort
import sqlite3

app = Flask(__name__)

isAdmin = False

DATABASE = 'sota.db'


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
    for topic in cursor.execute("""SELECT * FROM topics"""):
        print(topic)
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


def print_papers():
    connection = sqlite3.connect('sota.db')
    cursor = connection.cursor()
    for paper in cursor.execute("""SELECT * FROM papers"""):
        print(paper)
    connection.close()


@app.route('/add_paper', methods=['GET', 'POST'])
def add_paper():
    if request.method == 'POST':
        title = request.form["title"]
        abstract = request.form["abstract"]
        result = int(request.form["result"])
        topic_names = request.form.getlist('topic_names')
        sota_results = request.form.getlist('sota_results')
        author_names = request.form.getlist('author_names')
        author_surnames = request.form.getlist('author_surnames')

        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO papers (title, abstract, result) VALUES(?, ?, ?)""", (title, abstract, result))
        connection.commit()
        paper_id = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title,)).fetchall()[0][0]
        for topic_name, sota_result in zip(topic_names, sota_results):
            query_result = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=? AND sota_result=?""",
                                          (topic_name, sota_result)).fetchall()
            if not query_result:
                cursor.execute("""INSERT INTO topics (topic_name, sota_result) VALUES(?, ?)""",
                               (topic_name, sota_result))
                connection.commit()
            topic_id = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=? AND sota_result=?""",
                                      (topic_name, sota_result)).fetchall()[0][0]
            query_result = cursor.execute("""SELECT * FROM paper_topics WHERE paper_id=? AND topic_id=?""",
                                          (paper_id, topic_id)).fetchall()
            if not query_result:
                cursor.execute("""INSERT INTO paper_topics (paper_id, topic_id) VALUES(?, ?)""", (paper_id, topic_id))
                connection.commit()
        for author_name, author_surname in zip(author_names, author_surnames):
            query_result = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",
                                          (author_name, author_surname)).fetchall()
            if not query_result:
                cursor.execute("""INSERT INTO authors (author_name, author_surname) VALUES(?, ?)""",
                               (author_name, author_surname))
                connection.commit()
            author_id = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",
                                       (author_name, author_surname)).fetchall()[0][0]
            query_result = cursor.execute("""SELECT * FROM paper_authors WHERE paper_id=? AND author_id=?""",
                                          (paper_id, author_id)).fetchall()
            if not query_result:
                cursor.execute("""INSERT INTO paper_authors (paper_id, author_id) VALUES(?, ?)""",
                               (paper_id, author_id))
                connection.commit()
        connection.close()
        print_papers()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("add_paper.html")
    else:
        return abort(404)


@app.route('/update_paper', methods=['GET', 'POST'])
def update_paper():
    if request.method == 'POST':
        old_title = request.form["old_title"]
        new_title = request.form["new_title"]
        new_abstract = request.form["new_abstract"]
        new_result = int(request.form["new_result"])

        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE papers SET title=?, abstract=?, result=? WHERE title=?""",(new_title, new_abstract, new_result, old_title))
        connection.commit()
        connection.close()
        print_papers()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("update_paper.html")
    else:
        return abort(404)


@app.route('/delete_paper', methods=['GET', 'POST'])
def delete_paper():
    if request.method == 'POST':
        title = request.form["title"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM papers WHERE title=?""", (title,))
        connection.commit()
        connection.close()
        print_papers()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("delete_paper.html")
    else:
        return abort(404)

@app.route('/view_all', methods=['GET', 'POST'])
def view_all():
    if request.method == 'POST':
        view_all_for = request.form["view_all_for"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        rows = cursor.execute(f"SELECT * FROM {view_all_for}").fetchall()
        connection.close()
        return render_template("view_all.html", rows=rows)
    elif request.method == 'GET':
        return render_template("view_all.html", rows=[])
    else:
        return abort(404)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if isAdmin:
            if "author" in request.form:
                selected_option = request.form["author"]
                if selected_option == "add":
                    return redirect(url_for('add_author'))
                elif selected_option == "update":
                    return redirect(url_for('update_author'))
                elif selected_option == "delete":
                    return redirect(url_for('delete_author'))
                else:
                    return abort(404)
            elif "topic" in request.form:
                selected_option = request.form["topic"]
                if selected_option == "add":
                    return redirect(url_for('add_topic'))
                elif selected_option == "update":
                    return redirect(url_for('update_topic'))
                elif selected_option == "delete":
                    return redirect(url_for('delete_topic'))
                else:
                    return abort(404)
            elif "paper" in request.form:
                selected_option = request.form["paper"]
                if selected_option == "add":
                    return redirect(url_for('add_paper'))
                elif selected_option == "update":
                    return redirect(url_for('update_paper'))
                elif selected_option == "delete":
                    return redirect(url_for('delete_paper'))
                else:
                    return abort(404)
        else:
            option = request.form["option"]
            if option == "view_all":
                return redirect(url_for('view_all'))

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
