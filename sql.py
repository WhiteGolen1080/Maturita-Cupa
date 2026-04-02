# pip install mysql-connector
import mysql.connector

def get_connected():
    return mysql.connector.connect(
        host="dbs.spskladno.cz",
        user="student10",
        password="spsnet",
        database="vyuka10",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )

mydb = get_connected()
mydb.autocommit = True # to znamená že data budou furt aktualizovaný
mycursor = mydb.cursor(dictionary=True) # dictionary=True dělá že v html se to furt může udávat jako např {{ album.albumfile }}
mycursor.execute("SET NAMES utf8mb4")

def get_data(table):
    sql = f"SELECT * FROM {table}"
    mycursor.execute(sql)
    return mycursor.fetchall()



def insert_song(id, title, author, album, file, drive_id):
    sql = """
    INSERT INTO SONGS (id, title, author, album, songfile, drive_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """ # %s znamená basically že tam půjde nějaká věc (id, title, author, etc etc)

    data = (id, title, author, album, file, drive_id)
    mycursor.execute(sql, data) # vezme to sql a do těch %s dá data
    mydb.commit()

def delete_song(id):
    sql = """DELETE FROM PLAYLIST_SONG WHERE song_id = %s"""
    mycursor.execute(sql, (id,))
    sql = """DELETE FROM SONGS WHERE id = %s"""
    mycursor.execute(sql, (id,))
    mydb.commit()

def insert_post(id, user, content):
    sql = """
    INSERT INTO MATURITA_CUPA_POSTS (id, user, content)
    VALUES (%s, %s, %s)
    """

    data = (id, user, content)
    mycursor.execute(sql, data)
    mydb.commit()

def insert_user(id, username, display, email, password):
    sql = """
    INSERT INTO MATURITA_CUPA_USERS (id, username, display, email, password, following)
    VALUES (%s, %s, %s, %s, %s, "")
    """

    data = (id, username, display, email, password)
    mycursor.execute(sql, data)
    mydb.commit()

def create_individual_chat(name):
    sql = f"""
    CREATE TABLE {name} (
        id int PRIMARY KEY,
        content VARCHAR(255),
        sender VARCHAR(255)
    )
    """
    mycursor.execute(sql)
    mydb.commit()

def send_chat(id, content, sender, chat_id):
    sql = f"""
    INSERT INTO {chat_id} (id, content, sender)
    VALUES (%s, %s, %s)
    """

    data = (id, content, sender)
    mycursor.execute(sql, data)
    mydb.commit()

def update_text_color(username, color):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET textc = %s
    WHERE username = %s
    """

    data = (color, username)
    mycursor.execute(sql, data)
    mydb.commit()

def update_bg_color(username, color):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET backgroundc = %s
    WHERE username = %s
    """

    data = (color, username)
    mycursor.execute(sql, data)
    mydb.commit()

def update_border_color(username, color):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET borderc = %s
    WHERE username = %s
    """

    data = (color, username)
    mycursor.execute(sql, data)
    mydb.commit()

def update_disply_name(username, display):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET display = %s
    WHERE username = %s
    """

    data = (display, username)
    mycursor.execute(sql, data)
    mydb.commit()

def update_tags(username, tags):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET tags = %s
    WHERE username = %s
    """

    data = (tags, username)
    mycursor.execute(sql, data)
    mydb.commit()

def update_following(username, following):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET following = %s
    WHERE username = %s
    """

    data = (following, username)
    mycursor.execute(sql, data)
    mydb.commit()

def add_like(post_id):
    sql = """
    UPDATE MATURITA_CUPA_POSTS
    SET likes = likes + 1
    WHERE id = %s
    """

    data = (post_id,)
    mycursor.execute(sql, data)
    mydb.commit()

def add_follower(user):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET followers = followers + 1
    WHERE username = %s
    """

    data = (user,)
    mycursor.execute(sql, data)
    mydb.commit()

def remove_follower(user):
    sql = """
    UPDATE MATURITA_CUPA_USERS
    SET followers = followers - 1
    WHERE username = %s
    """

    data = (user,)
    mycursor.execute(sql, data)
    mydb.commit()