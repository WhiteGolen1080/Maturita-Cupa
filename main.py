from flask import Flask, request, render_template, redirect, session, url_for, make_response, jsonify, abort
import uuid
import os
import json
import re

from sql import insert_post, get_data, insert_user, update_text_color, update_bg_color, update_border_color, update_disply_name, update_tags, add_like, update_following, add_follower, remove_follower

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/data")
app.config["SECRET_KEY"] = "123456789"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "tajnyklic"

def extract_nameplate(text):
    match = re.search(r"\[nameplate:(.*?)\]", text)

    if match:
        nameplate = match.group(1)
        cleaned_text = re.sub(r"\[nameplate:.*?\]", "", text).strip()
        return nameplate, cleaned_text

    return None, text

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
    posts = get_data("MATURITA_CUPA_POSTS")
    users = get_data("MATURITA_CUPA_USERS")
    username = session.get("user")
    role = session.get("role")

    user_text_colors = {
        user['username']: user['textc']
        for user in users
    }

    user_background_colors = {
        user['username']: user['backgroundc']
        for user in users
    }

    user_border_colors = {
        user["username"]: user["borderc"]
        for user in users
    }

    for post in posts:
        post['textc'] = user_text_colors.get(post['user'], "F0FFFF")
        post['backgroundc'] = user_background_colors.get(post['user'], "1E1E1E")
        post['borderc'] = user_border_colors.get(post['user'], "0F0F0F")

    return render_template("index.html", posts=posts, username=username, role=role, users=users)

@app.route('/following')
def index_following():
    posts = get_data("MATURITA_CUPA_POSTS")
    users = get_data("MATURITA_CUPA_USERS")
    username = session.get("user")
    role = session.get("role")

    user_text_colors = {
        user['username']: user['textc']
        for user in users
    }

    user_background_colors = {
        user['username']: user['backgroundc']
        for user in users
    }

    user_border_colors = {
        user["username"]: user["borderc"]
        for user in users
    }

    for post in posts:
        post['textc'] = user_text_colors.get(post['user'], "F0FFFF")
        post['backgroundc'] = user_background_colors.get(post['user'], "1E1E1E")
        post['borderc'] = user_border_colors.get(post['user'], "0F0F0F")

    for u in users:
        if u["username"] == username:
            if u["following"] == None:
                return render_template("index.html", posts=posts, username=username, role=role, users=users)

    return render_template("index_following.html", posts=posts, username=username, role=role, users=users)

@app.route('/send-post', methods=["POST"])
def send_post():
    username = session.get("user")
    content = request.form.get("post_content")

    post_id = 0

    posty = get_data("MATURITA_CUPA_POSTS")
    for p in posty:
        if p["id"] == post_id:
            post_id += 1

    novy_post = {
        "username": username,
        "content": content,
        "code": post_id,
    }
    insert_post(post_id, username, content)
    # note to self: jde jich dysplaynout max 5 + ten hard coded
    return redirect(url_for("index"))

@app.route('/search')
def search():
    users = get_data("MATURITA_CUPA_USERS")
    return render_template("search.html", users=users)

@app.route('/set_filter', methods=["POST"])
def set_filter():
    username = session.get("user")
    filter = request.form.get("search_filter").lstrip('#')

    print(filter)
    if filter is None or filter == "":
        print("redirecting no filter")
        return redirect(url_for("search"))
    else:
        print("redirecting with filter ''" + filter + "''")
        return redirect("search/filter/" + filter)

@app.route('/search/filter/<string:search_by>', methods=["GET"])
def filter_search(search_by):
    users = get_data("MATURITA_CUPA_USERS")
    filter = search_by
    return render_template("filter_search.html", users=users, filter=filter)

@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username_or_email = request.form.get("username")
        password = request.form.get("password")

        users = get_data("MATURITA_CUPA_USERS")
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

        user_id = generate_id()

        users = read_json("users")
        #for u in users:
            #if u["email"] == email:
                #return redirect(url_for("login"))

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
        insert_user(user_id, username, username, email, password)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/profile')
def profile():
    username = session.get("user")
    users = get_data("MATURITA_CUPA_USERS")
    posts = get_data("MATURITA_CUPA_POSTS")

    user_text_colors = {
        user['username']: user['textc']
        for user in users
    }

    user_background_colors = {
        user['username']: user['backgroundc']
        for user in users
    }

    user_border_colors = {
        user["username"]: user["borderc"]
        for user in users
    }

    for post in posts:
        post['textc'] = user_text_colors.get(post['user'], "F0FFFF")
        post['backgroundc'] = user_background_colors.get(post['user'], "1E1E1E")
        post['borderc'] = user_border_colors.get(post['user'], "0F0F0F")

    for user in users:
        display = user["username"]

        if user["tags"] is not None:
            display, clean = extract_nameplate(user["tags"])
            print(display)
            print(clean)
            if display is None:
                display = user["username"]

            if user["role"] == "admin":
                display = display + "🛡️"

            if user["username"] == "Toney":
                display = display + "🎶"

            if "[fire]" in user["tags"]:
                display = display + "🔥"
            if "[cat]" in user["tags"]:
                display = display + "😺"
            if "[love]" in user["tags"]:
                display = display + "❤"
            if "[red_heart]" in user["tags"]:
                display = display + "❤️"
            if "[pink_heart]" in user["tags"]:
                display = display + "🩷"
            if "[blue_heart]" in user["tags"]:
                display = display + "💙"
            if "[purple_heart]" in user["tags"]:
                display = display + "💜"
            if "[black_heart]" in user["tags"]:
                display = display + "🖤"
            if "[note]" in user["tags"]:
                display = display + "🎵"
        else:
            update_tags(user["username"], "")

        update_disply_name(user["username"], display)

    users = get_data("MATURITA_CUPA_USERS")

    return render_template("profile.html", username=username, users=users, posts=posts)

@app.route('/profile/browse/<string:users_name>')
def other_profile(users_name):
    username = session.get("user")
    users = get_data("MATURITA_CUPA_USERS")
    posts = get_data("MATURITA_CUPA_POSTS")
    looking_at = users_name

    user_text_colors = {
        user['username']: user['textc']
        for user in users
    }

    user_background_colors = {
        user['username']: user['backgroundc']
        for user in users
    }

    user_border_colors = {
        user["username"]: user["borderc"]
        for user in users
    }

    for post in posts:
        post['textc'] = user_text_colors.get(post['user'], "F0FFFF")
        post['backgroundc'] = user_background_colors.get(post['user'], "1E1E1E")
        post['borderc'] = user_border_colors.get(post['user'], "0F0F0F")

    users = get_data("MATURITA_CUPA_USERS")

    return render_template("other_profile.html", username=username, users=users, posts=posts, looking_at=looking_at)

@app.route('/set_textc', methods=["POST"])
def set_textc():
    username = session.get("user")
    color = request.form.get("text_color").lstrip('#')

    print(color)
    update_text_color(username, color)
    return redirect(url_for("profile"))

@app.route('/set_bgc', methods=["POST"])
def set_bgc():
    username = session.get("user")
    color = request.form.get("background_color").lstrip('#')

    print(color)
    update_bg_color(username, color)
    return redirect(url_for("profile"))

@app.route('/set_borderc', methods=["POST"])
def set_borderc():
    username = session.get("user")
    color = request.form.get("border_color").lstrip('#')

    print(color)
    update_border_color(username, color)
    return redirect(url_for("profile"))

@app.route('/set_tags', methods=["POST"])
def set_tags():
    username = session.get("user")
    tags = request.form.get("tags").lstrip('#')

    print(tags)
    update_tags(username, tags)
    return redirect(url_for("profile"))

@app.route('/copy_textc/<string:user>', methods=["POST"])
def copy_textc(user):
    username = session.get("user")
    original_user = user
    users = get_data("MATURITA_CUPA_USERS")

    for u in users:
        if u["username"] == original_user:
            color = u["textc"]

    update_text_color(username, color)
    return redirect("../../profile/browse/"+original_user)

@app.route('/copy_bgc/<string:user>', methods=["POST"])
def copy_bgc(user):
    username = session.get("user")
    original_user = user
    users = get_data("MATURITA_CUPA_USERS")

    for u in users:
        if u["username"] == original_user:
            color = u["backgroundc"]

    update_bg_color(username, color)
    return redirect("../../profile/browse/"+original_user)

@app.route('/copy_borderc/<string:user>', methods=["POST"])
def copy_borderc(user):
    username = session.get("user")
    original_user = user
    users = get_data("MATURITA_CUPA_USERS")

    for u in users:
        if u["username"] == original_user:
            color = u["borderc"]

    update_border_color(username, color)
    return redirect("../../profile/browse/"+original_user)

@app.route('/like_post/<int:post>', methods=["GET"])
def like_post(post):
    username = session.get("user")
    post_id = post
    users = get_data("MATURITA_CUPA_USERS")

    add_like(post_id)
    return redirect(url_for("index"))

@app.route('/follow_person/<string:person>', methods=["GET"])
def follow_person(person):
    username = session.get("user")
    person = person
    users = get_data("MATURITA_CUPA_USERS")

    for u in users:
        if u["username"] == username:
            following = u["following"]
            if u["following"] == None:
                following = following + person
            else:
                following = following + ", " + person

    update_following(username, following)
    add_follower(person)
    return redirect("../../profile/browse/"+person)

@app.route('/unfollow_person/<string:person>', methods=["GET"])
def unfollow_person(person):
    username = session.get("user")
    person = person
    users = get_data("MATURITA_CUPA_USERS")

    for u in users:
        if u["username"] == username:
            following = u["following"].replace(person, "")

    update_following(username, following)
    remove_follower(person)
    return redirect("../../profile/browse/"+person)

if __name__ == "__main__":
    app.run(debug=True)