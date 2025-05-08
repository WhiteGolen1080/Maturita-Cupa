from flask import Flask, request, render_template, redirect, session, url_for, make_response, jsonify, abort
import uuid
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/data")
app.config["SECRET_KEY"] = "123456789"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "tajnyklic"

def read_json(file_name):
    active_file = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(active_file)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{file_name}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    return USERS
def write_json(file_name, data_to_write):
    active_file = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(active_file)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{file_name}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    USERS.append(data_to_write)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(USERS, outline, indent=2)

    return

def generate_id():
    return str(uuid.uuid4())

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username_or_email = request.form.get("username")
        password = request.form.get("password")

        users = read_json("users")
        for u in users:
            if u["username"] == username_or_email or u["email"] == username_or_email and u["password"] == password:
                session["user"] = u["username"]
                session["role"] = u["role"]
                return redirect(url_for("profile"))

        return render_template("login.html", error="Incorrect name or password")

    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("role", None)
    return redirect(url_for("index"))

@app.route('/register', methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        role = "user"

        users = read_json("users")
        for u in users:
            if u["email"] == email:
                return redirect(url_for("login"))

        new_user = {
            "username": username,
            "display-name": username,
            "email": email,
            "password": password,
            "role": role,
            "tags": "",
            "badges": [],
            "followers": 0,
            "following": 0
        }
        write_json("users", new_user)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)