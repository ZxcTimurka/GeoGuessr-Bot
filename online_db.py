import sqlite3


def create_table():
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS players(
                        name TEXT,
                        time INTEGER,
                        score INTEGER,
                        image_id INTEGER
                    )
                ''')


def add_player(name, time, score, image_id):
    con = sqlite3.connect('players.db')
    with con:
        data = con.execute("select count(*) from sqlite_master where type='table' and name='goods'")
        for row in data:
            if row[0] == 0:
                create_table()
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                            INSERT INTO players(name, time, score, image_id) VALUES(?, ?, ?, ?)
                        ''', (name, time, score, image_id))
                    con.commit()
            else:
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                            INSERT INTO players(name, time, score, image_id) VALUES(?, ?, ?, ?)
                        ''', (name, time, score, image_id))
                    con.commit()


def print_time(name, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time FROM players WHERE name = ? and image_id = ?""", (name, image_id)).fetchall()
    for elem in result:
        return elem


def print_score(name, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT score FROM players WHERE name = ? and image_id = ?""", (name, image_id)).fetchall()
    for elem in result:
        return elem


def print_imageid(name, time, score):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT image_id FROM players WHERE name = ? and time = ? and score = ?""",
                         (name, time, score)).fetchall()
    for elem in result:
        return elem
