from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{"name": "Home","url": "index"},
        {"name": "About THE Project","url": "about"},
        ]

@app.route("/index")
@app.route("/")
def index():
    print(url_for("index"))
    return render_template("index.html", title="HomE", menu=menu)

@app.route("/about")
def about():
    print(url_for("about"))
    return render_template("about.html", title="About THE Project", menu=menu)

@app.route("/profile/<username>")
def profile(username):
    return f"Пользователь: {username}"

if __name__ == '__main__':
    app.run(debug=True)