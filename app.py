from flask import Flask, render_template, redirect, url_for, g, request, abort
import sqlite3

app = Flask(__name__)

isAdmin = False

DATABASE = 'sota.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
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
