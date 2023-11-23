import sqlite3
import os
from flask import Flask, render_template, g
from  flaskos.flskDB import FlaskoDB

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
    return render_template("index.html", title="HomE", menu=dbase.get_menu())

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