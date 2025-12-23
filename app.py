from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

ADMIN_USERNAME = "DasariMurali123"
ADMIN_PASSWORD = "Dasari@123"


def get_db():
    return sqlite3.connect("database.db")


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM crops")
    crops = cursor.fetchall()
    db.close()
    return render_template("index.html", crops=crops)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == ADMIN_USERNAME and
                request.form["password"] == ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add_crop():
    if not session.get("admin"):
        return redirect(url_for("index"))
    name = request.form["name"]
    price = request.form["price"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO crops (name, price) VALUES (?, ?)", (name, price))
    db.commit()
    db.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_crop(id):
    if not session.get("admin"):
        return redirect(url_for("index"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM crops WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["POST"])
def edit_crop(id):
    if not session.get("admin"):
        return redirect(url_for("index"))
    price = request.form["price"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE crops SET price=? WHERE id=?", (price, id))
    db.commit()
    db.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
