import sqlite3
import os
from flask import Flask, render_template, g, url_for, request, flash, session, redirect, abort
from flaskos.flskDB import FlaskoDB

DATABASE = 'flasko.db'
DEBUG = True
SECRET_KEY = '72b81b22e0c3f3714a2b5cc217a912193da0eeab'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsako.db")))

def connect_bd():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con

def create_db():
    db = connect_bd()
    with app.open_resource("db_fl.sql", "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_bd()
    return g.link_db

@app.route("/")
def index():
    db = get_db()
    dbase = FlaskoDB(db)
    return render_template("index.html", title="HomE", menu=dbase.get_menu(),posts=dbase.get_posts_anonce())

@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FlaskoDB(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Ошибка добавления статьи!", category='error')
            else: flash("Статья добавлена успешно!", category='success')
        else:
            flash("Ошибка добавления статьи!", category='error')

    return render_template("add_post.html", title="Add Article", menu=dbase.get_menu())


@app.route("/posts/<alias>")
def show_post(alias):
    db = get_db()
    dbase = FlaskoDB(db)
    post_data = dbase.get_post(alias)



    if not post_data:
        print(f"No data found for alias '{alias}'")  # Добавьте это для отладки
        abort(404)

    indtificator = post_data['id']
    title = post_data['title']
    text = post_data['text']

    return render_template("post.html", menu=dbase.get_menu(), title=title, post_data=post_data)


@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    db = get_db()
    dbase = FlaskoDB(db)
    success = dbase.delete_post(post_id)

    return redirect(url_for('index'))

@app.route("/about")
def about():
    db = get_db()
    dbase = FlaskoDB(db)
    return render_template("about.html", title="About THE Project", menu=dbase.get_menu())

@app.route("/profile/<username>")
def profile(username):
    return f"Пользователь: {username}"

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == '__main__':
    app.run(debug=True)