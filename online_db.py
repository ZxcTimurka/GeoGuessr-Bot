import sqlite3


def create_table():
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS players(
                        id INTEGER,
                        name TEXT,
                        time INTEGER,
                        score INTEGER,
                        image_id INTEGER,
                        curr_img TEXT
                    )
                ''')


def update_curr_img(id, img):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, img)
        cursor.execute(f"""update players set curr_img = '{img}' where id = {id}""")
        con.commit()


def add_player(id, name, time, score, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f'''select * from players where id = {id}''').fetchall()
    if not result:
        with con:
            data = con.execute("select count(*) from sqlite_master where type='table' and name='goods'")
            for row in data:
                if row[0] == 0:
                    create_table()
                    with con:
                        cursor = con.cursor()
                        cursor.execute('''
                            INSERT INTO players(id, name, time, score, image_id, curr_img) VALUES(?, ?, ?, ?, ?, ?)
                        ''', (id, name, time, score, image_id, None))
                        con.commit()
                else:
                    with con:
                        cursor = con.cursor()
                        cursor.execute('''
                              INSERT INTO players(id, name, time, score, image_id, curr_img) VALUES(?, ?, ?, ?, ?, ?)
                         ''', (id, name, time, score, image_id, None))
                        con.commit()


def print_time(id, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time FROM players WHERE id = ? and image_id = ?""", (id, image_id)).fetchall()
    for elem in result:
        return elem


def print_score(id, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT score FROM players WHERE id = ? and image_id = ?""", (id, image_id)).fetchall()
    for elem in result:
        return elem


def print_imageid(id, time, score):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT image_id FROM players WHERE id = ? and time = ? and score = ?""",
                         (id, time, score)).fetchall()
    for elem in result:
        return elem


def print_curr_img(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT curr_img FROM players WHERE id = {id}""").fetchall()
    for elem in result:
        return elem


create_table()