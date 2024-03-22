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
                        curr_img TEXT,
                        time_bool TEXT,
                        in_searching INTEGER
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
                            INSERT INTO players(id, name, time, score, image_id, curr_img, time_bool) VALUES(?, ?, ?, ?, ?, ?, ?)
                        ''', (id, name, time, score, image_id, None, False))
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

#для режима на время
def print_time_bool(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT time_bool FROM players WHERE id = {id}""").fetchall()
    for elem in result:
        return elem


def update_time_bool(id, bool):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, bool)
        cursor.execute(f"""update players set time_bool = '{bool}' where id = {id}""")
        con.commit()


def change_search(id):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        result = cursor.execute(f"""SELECT in_searching FROM players WHERE id = {id}""").fetchall()[0]
        cursor.execute(f"""update players set in_searching = 0 where id = {id}""" if result else f"""update players set in_searching = 1 where id = {id}""")
        con.commit()


def print_ready():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT id FROM players WHERE in_searching = 1""").fetchall()
    for elem in result:
        return elem

create_table()