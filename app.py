from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

isAdmin = False


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/index')
def index():
    return render_template("index.html")


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
