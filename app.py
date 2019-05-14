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
        author_name = request.form["author_name"]
        author_surname = request.form["author_surname"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_result = cursor.execute("""SELECT * FROM authors WHERE author_name=? AND author_surname=?""", (author_name, author_surname)).fetchone()
        if not query_result:
            cursor.execute("""INSERT INTO authors (author_name, author_surname) VALUES(?, ?)""", (author_name, author_surname))
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
        query_result = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""", (author_name, author_surname)).fetchone()
        if query_result:
            author_id = query_result[0]
            cursor.execute("""DELETE FROM authors WHERE author_id=?""", (author_id,))
            cursor.execute("""DELETE FROM paper_authors WHERE author_id=?""", (author_id, ))
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
        sota_result = -1
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_result = cursor.execute("""SELECT * FROM topics WHERE topic_name=?""", (topic_name,)).fetchone()
        if not query_result:
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
        new_topic_name = request.form["new_topic_name"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE topics SET topic_name=? WHERE topic_name=?""", (new_topic_name, old_topic_name))
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
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_result = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""", (topic_name,)).fetchone()
        if query_result:
            topic_id = query_result[0]
            cursor.execute("""DELETE FROM topics WHERE topic_id=?""", (topic_id,))
            cursor.execute("""DELETE FROM paper_topics WHERE topic_id=?""", (topic_id,))
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
        title = request.form["title"].strip()
        abstract = request.form["abstract"].strip()
        result = int(request.form["result"].strip())
        topic_names = request.form.getlist('topic_names')
        author_names = request.form.getlist('author_names')
        author_surnames = request.form.getlist('author_surnames')

        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO papers (title, abstract, result) VALUES(?, ?, ?)""", (title, abstract, result))
        connection.commit()
        paper_id = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title,)).fetchone()[0]
        for topic_name in topic_names:
            topic_name = topic_name.strip()
            query_result = cursor.execute("""SELECT sota_result FROM topics WHERE topic_name=?""",(topic_name,)).fetchone()
            if query_result:
                curr_result = query_result[0]
                if result > curr_result:
                    cursor.execute("""UPDATE topics SET sota_result=? WHERE topic_name=?""",(result, topic_name))
            else:
                cursor.execute("""INSERT INTO topics (topic_name, sota_result) VALUES(?, ?)""", (topic_name, result))
            connection.commit()

            topic_id = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""", (topic_name,)).fetchone()[0]

            cursor.execute("""INSERT INTO paper_topics (paper_id, topic_id) VALUES(?, ?)""", (paper_id, topic_id))
            connection.commit()
        for author_name, author_surname in zip(author_names, author_surnames):
            author_name = author_name.strip()
            author_surname = author_surname.strip()
            query_result = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",
                                          (author_name, author_surname)).fetchone()
            if not query_result:
                cursor.execute("""INSERT INTO authors (author_name, author_surname) VALUES(?, ?)""", (author_name, author_surname))
                connection.commit()
            author_id = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""", (author_name, author_surname)).fetchone()[0]

            cursor.execute("""INSERT INTO paper_authors (paper_id, author_id) VALUES(?, ?)""", (paper_id, author_id))
            connection.commit()
        connection.close()
        print_papers()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("add_paper.html")
    else:
        return abort(404)

@app.route('/update_title', methods=['GET', 'POST'])
def update_title():
    if request.method == 'POST':
        old_title_name = request.form['old_title_name']
        new_title_name = request.form['new_title_name']
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_result = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (new_title_name, )).fetchone()
        if not query_result:
            cursor.execute("""UPDATE papers SET title=? WHERE title=?""", (new_title_name, old_title_name))
            connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('update_title.html')
    else:
        return abort(404)

@app.route('/update_abstract', methods=['GET', 'POST'])
def update_abstract():
    if request.method == 'POST':
        title = request.form['title'].strip()
        abstract = request.form['abstract'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE papers SET abstract=? WHERE title=?""", (abstract, title))
        connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('update_abstract.html')
    else:
        return abort(404)

@app.route('/update_sota_result', methods=['GET', 'POST'])
def update_sota_result():
    if request.method == 'POST':
        title = request.form['title'].strip()
        new_result = int(request.form['new_result'].strip())
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE papers SET result=? WHERE title=?""", (new_result, title))
        connection.commit()
        query_result = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title,)).fetchone()
        if query_result:
            paper_id = query_result[0]
            query_result = cursor.execute("""SELECT topic_id FROM paper_topics WHERE paper_id=?""", (paper_id, )).fetchall()
            for query_tuple in query_result:
                topic_id = query_tuple[0]
                max_result = -1
                max_tuple = cursor.execute("""SELECT MAX(result) FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=?""", (topic_id,)).fetchone()
                if max_tuple:
                    max_result = max_tuple[0]
                cursor.execute("""UPDATE topics SET sota_result=? WHERE topic_id=?""", (max_result, topic_id))
                connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('update_sota_result.html')
    else:
        return abort(404)

@app.route('/paper_add_author', methods=['GET', 'POST'])
def paper_add_author():
    if request.method == 'POST':
        title = request.form['title'].strip()
        new_author_name = request.form['new_author_name'].strip()
        new_author_surname = request.form['new_author_surname'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()

        query_tuple = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title, )).fetchone()
        if query_tuple:
            paper_id = query_tuple[0]

            query_tuple = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",(new_author_name, new_author_surname)).fetchone()
            if not query_tuple:
                cursor.execute("""INSERT INTO authors (author_name, author_surname) VALUES(?, ?)""", (new_author_name, new_author_surname))
                connection.commit()
            author_id = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",(new_author_name, new_author_surname)).fetchone()[0]

            query_tuple = cursor.execute("""SELECT * FROM paper_authors WHERE paper_id=? AND author_id=?""",(paper_id, author_id)).fetchone()

            if not query_tuple:
                cursor.execute("""INSERT INTO paper_authors (paper_id, author_id) VALUES(?, ?)""", (paper_id, author_id))
                connection.commit()

        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_add_author.html')
    else:
        return abort(404)

@app.route('/paper_update_author', methods=['GET', 'POST'])
def paper_update_author():
    if request.method == 'POST':
        old_author_name = request.form['old_author_name'].strip()
        old_author_surname = request.form['old_author_surname'].strip()
        new_author_name = request.form['new_author_name'].strip()
        new_author_surname = request.form['new_author_surname'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE authors SET author_name=?, author_surname=? WHERE author_name=? AND author_surname=?""", (new_author_name, new_author_surname, old_author_name, old_author_surname))
        connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_update_author.html')
    else:
        return abort(404)

@app.route('/paper_delete_author', methods=['GET', 'POST'])
def paper_delete_author():
    if request.method == 'POST':
        title = request.form['title'].strip()
        author_name = request.form['author_name'].strip()
        author_surname = request.form['author_surname'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()

        query_tuple = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title, )).fetchone()
        if query_tuple:
            paper_id = query_tuple[0]

            query_tuple = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""",(author_name, author_surname)).fetchone()
            if query_tuple:
                author_id = query_tuple[0]
                cursor.execute("""DELETE FROM paper_authors WHERE paper_id=? AND author_id=?""", (paper_id, author_id))
                connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_delete_author.html')
    else:
        return abort(404)

@app.route('/paper_add_topic', methods=['GET', 'POST'])
def paper_add_topic():
    if request.method == 'POST':
        title = request.form['title'].strip()
        topic_name = request.form['new_topic_name'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()

        query_tuple = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title, )).fetchone()
        if query_tuple:
            paper_id = query_tuple[0]

            query_tuple = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""",(topic_name,)).fetchone()
            if not query_tuple:
                cursor.execute("""INSERT INTO topics (topic_name, sota_result) VALUES(?, ?)""", (topic_name, -1))
                connection.commit()
            topic_id = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""",(topic_name,)).fetchone()[0]

            query_tuple = cursor.execute("""SELECT * FROM paper_topics WHERE paper_id=? AND topic_id=?""",(paper_id, topic_id)).fetchone()

            if not query_tuple:
                cursor.execute("""INSERT INTO paper_topics (paper_id, topic_id) VALUES(?, ?)""", (paper_id, topic_id))
                connection.commit()

            max_result = -1
            max_tuple = cursor.execute(
                """SELECT MAX(result) FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=?""",
                (topic_id,)).fetchone()
            if max_tuple:
                max_result = max_tuple[0]
            cursor.execute("""UPDATE topics SET sota_result=? WHERE topic_id=?""", (max_result, topic_id))
            connection.commit()

        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_add_topic.html')
    else:
        return abort(404)

@app.route('/paper_update_topic', methods=['GET', 'POST'])
def paper_update_topic():
    if request.method == 'POST':
        old_topic_name = request.form['old_topic_name'].strip()
        new_topic_name = request.form['new_topic_name'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE topics SET topic_name=? WHERE topic_name=?""", (new_topic_name, old_topic_name))
        connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_update_topic.html')
    else:
        return abort(404)

@app.route('/paper_delete_topic', methods=['GET', 'POST'])
def paper_delete_topic():
    if request.method == 'POST':
        title = request.form['title'].strip()
        topic_name = request.form['topic_name'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_tuple = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title, )).fetchone()
        if query_tuple:
            paper_id = query_tuple[0]
            query_tuple = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""",(topic_name,)).fetchone()
            if query_tuple:
                topic_id = query_tuple[0]
                cursor.execute("""DELETE FROM paper_topics WHERE paper_id=? AND topic_id=?""", (paper_id, topic_id))
                connection.commit()

                max_result = -1
                max_tuple = cursor.execute(
                    """SELECT MAX(result) FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=?""",
                    (topic_id,)).fetchone()
                if max_tuple:
                    max_result = max_tuple[0]
                cursor.execute("""UPDATE topics SET sota_result=? WHERE topic_id=?""", (max_result, topic_id))
                connection.commit()
        connection.close()
        return redirect(url_for('update_paper'))
    elif request.method == 'GET':
        return render_template('paper_delete_topic.html')
    else:
        return abort(404)

@app.route('/update_paper', methods=['GET', 'POST'])
def update_paper():
    if request.method == 'POST':
        option = request.form["option"]
        if option == "update_title":
            return redirect(url_for("update_title"))
        elif option == "update_abstract":
            return redirect(url_for("update_abstract"))
        elif option == "update_sota_result":
            return redirect(url_for("update_sota_result"))
        elif option == "paper_add_author":
            return redirect(url_for("paper_add_author"))
        elif option == "paper_update_author":
            return redirect(url_for("paper_update_author"))
        elif option == "paper_delete_author":
            return redirect(url_for("paper_delete_author"))
        elif option == "paper_add_topic":
            return redirect(url_for("paper_add_topic"))
        elif option == "paper_update_topic":
            return redirect(url_for("paper_update_topic"))
        elif option == "paper_delete_topic":
            return redirect(url_for("paper_delete_topic"))
        else:
            return abort(404)
    elif request.method == 'GET':
        return render_template("update_paper_index.html")
    else:
        return abort(404)


@app.route('/delete_paper', methods=['GET', 'POST'])
def delete_paper():
    if request.method == 'POST':
        title = request.form["title"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        query_result = cursor.execute("""SELECT paper_id FROM papers WHERE title=?""", (title,)).fetchone()
        if query_result:
            paper_id = query_result[0]
            cursor.execute("""DELETE FROM papers WHERE paper_id=?""", (paper_id,))
            query_result = cursor.execute("""SELECT topic_id FROM paper_topics WHERE paper_id=?""", (paper_id,)).fetchall()
            cursor.execute("""DELETE FROM paper_topics WHERE paper_id=?""", (paper_id,))
            connection.commit()
            for query_tuple in query_result:
                topic_id = query_tuple[0]
                max_result = -1
                max_tuple = cursor.execute("""SELECT MAX(result) FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=?""", (topic_id,)).fetchone()
                if max_tuple:
                    max_result = max_tuple[0]
                cursor.execute("""UPDATE topics SET sota_result=? WHERE topic_id=?""", (max_result, topic_id))
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
        return render_template("view_all.html", rows=rows, option=view_all_for)
    elif request.method == 'GET':
        return render_template("view_all.html", rows=[], option="none")
    else:
        return abort(404)

@app.route('/papers_by_author', methods=['GET', 'POST'])
def papers_by_author():
    if request.method == 'POST':
        author_name = request.form["author_name"]
        author_surname = request.form["author_surname"]
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT author_id FROM authors WHERE author_name=? and author_surname=?", (author_name, author_surname)).fetchall()
        papers = []
        if result:
            author_id = result[0][0]
            result = cursor.execute(f"SELECT paper_id FROM paper_authors WHERE author_id={author_id}").fetchall()
            if result:
                paper_ids = [element[0] for element in result]
                for paper_id in paper_ids:
                    papers.extend(cursor.execute(f"SELECT * FROM papers WHERE paper_id={paper_id}").fetchall())
        connection.close()
        return render_template("papers_by_author.html", papers=papers)
    elif request.method == 'GET':
        return render_template("papers_by_author.html", papers=[])
    else:
        return abort(404)

@app.route('/rank_all_authors', methods=['GET'])
def rank_all_authors():
    if request.method == 'GET':
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        D = {}
        #authors_with_rank = cursor.execute("""SELECT author_name, author_surname, COUNT(*) FROM authors INNER JOIN paper_authors ON authors.author_id = paper_authors.author_id GROUP BY author_name, author_surname""").fetchall()
        authors_with_rank = []
        query_result_1 = cursor.execute("""SELECT topic_id, sota_result FROM topics""").fetchall()
        for query_tuple_1 in query_result_1:
            topic_id = query_tuple_1[0]
            sota_result = query_tuple_1[1]
            query_result_2 = cursor.execute("""SELECT paper_id FROM paper_topics WHERE topic_id=?""", (topic_id,)).fetchall()
            for query_tuple_2 in query_result_2:
                paper_id = query_tuple_2[0]

                query_result_3 = cursor.execute("""SELECT paper_id FROM papers WHERE paper_id=? AND result=?""", (paper_id, sota_result)).fetchall()
                for query_tuple_3 in query_result_3:
                    paper_id_sota_achieved = query_tuple_3[0]
                    query_result_4 = cursor.execute("""SELECT author_name, author_surname FROM authors INNER JOIN paper_authors ON authors.author_id=paper_authors.author_id WHERE paper_id=?""", (paper_id_sota_achieved, )).fetchall()
                    for query_tuple_4 in query_result_4:
                        if query_tuple_4 in D:
                            D[query_tuple_4] += 1
                        else:
                            D[query_tuple_4] = 1

        authors = cursor.execute("""SELECT author_name, author_surname FROM authors""").fetchall()
        authors_with_rank = []
        for author in authors:
            if author in D:
                authors_with_rank.append((D[author], author[0], author[1]))
            else:
                authors_with_rank.append((0, author[0], author[1]))
        authors_with_rank.sort(reverse=True)
        return render_template("rank_all_authors.html", authors_with_rank=authors_with_rank)
    else:
        return abort(404)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword'].strip()
        pattern = '%' + keyword + '%'
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        papers = cursor.execute("""SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ?""", (pattern, pattern)).fetchall()
        connection.close()
        return render_template("search.html", papers=papers)
    elif request.method == 'GET':
        return render_template("search.html", papers = [])
    else:
        return abort(404)

@app.route('/papers_by_topic', methods=['GET', 'POST'])
def papers_by_topic():
    if request.method == 'POST':
        topic_name = request.form['topic_name'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        papers = []
        query_result = cursor.execute("""SELECT topic_id FROM topics WHERE topic_name=?""", (topic_name,)).fetchone()
        if query_result:
            topic_id = query_result[0]
            papers = cursor.execute("""SELECT papers.title, papers.abstract, papers.result FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=?""", (topic_id,)).fetchall()
        connection.close()
        return render_template("papers_by_topic.html", papers=papers)
    elif request.method == 'GET':
        return render_template("papers_by_topic.html", papers = [])
    else:
        return abort(404)

@app.route('/sota_by_topic', methods=['GET', 'POST'])
def sota_by_topic():
    if request.method == 'POST':
        topic_name = request.form['topic_name'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        papers = []
        query_result = cursor.execute("""SELECT topic_id, sota_result FROM topics WHERE topic_name=?""", (topic_name,)).fetchone()
        if query_result:
            topic_id = query_result[0]
            sota_result = query_result[1]
            papers = cursor.execute("""SELECT papers.title, papers.abstract, papers.result FROM papers INNER JOIN paper_topics ON papers.paper_id=paper_topics.paper_id WHERE topic_id=? and result=?""", (topic_id, sota_result)).fetchall()
        connection.close()
        return render_template("sota_by_topic.html", papers=papers)
    elif request.method == 'GET':
        return render_template("sota_by_topic.html", papers = [])
    else:
        return abort(404)

@app.route('/view_coauthors', methods=['GET', 'POST'])
def view_coauthors():
    if request.method == 'POST':
        author_name = request.form['author_name'].strip()
        author_surname = request.form['author_surname'].strip()
        connection = sqlite3.connect('sota.db')
        cursor = connection.cursor()
        coauthors = []
        query_result = cursor.execute("""SELECT author_id FROM authors WHERE author_name=? AND author_surname=?""", (author_name, author_surname)).fetchone()
        if query_result:
            author_id = query_result[0]
            query_result = cursor.execute("""SELECT paper_id FROM paper_authors WHERE author_id=?""", (author_id,)).fetchall()
            if query_result:
                for query_tuple in query_result:
                    paper_id = query_tuple[0]
                    coauthors.extend(cursor.execute("""SELECT DISTINCT author_name, author_surname FROM authors INNER JOIN paper_authors ON authors.author_id=paper_authors.author_id WHERE paper_id=? and authors.author_id!=?""",
                                                  (paper_id, author_id)).fetchall())
        connection.close()
        return render_template("view_coauthors.html", coauthors=set(coauthors))
    elif request.method == 'GET':
        return render_template("view_coauthors.html", coauthors = [])
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
            elif option == "papers_by_author":
                return redirect(url_for('papers_by_author'))
            elif option == "rank_all_authors":
                return redirect(url_for('rank_all_authors'))
            elif option == "search":
                return redirect(url_for('search'))
            elif option == "papers_by_topic":
                return redirect(url_for('papers_by_topic'))
            elif option == "sota_by_topic":
                return redirect(url_for('sota_by_topic'))
            elif option == "view_coauthors":
                return redirect(url_for('view_coauthors'))
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
