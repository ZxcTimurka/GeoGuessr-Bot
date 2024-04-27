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
                        time_bool INTEGER,
                        in_searching INTEGER,
                        pair INTEGER,
                        suggest_stage INTEGER,
                        online_imgs TEXT,
                        online_score INTEGER,
                        time_score
                    )
                ''')


def update_curr_img(id, img):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, img)
        cursor.execute(f"""update players set curr_img = '{img}' where id = {id}""")
        con.commit()


def add_player(id, name):
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
                            INSERT INTO players(id, name, time, score, image_id, curr_img, time_bool, time_score) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (id, name, 0, 0, 0, None, False, 0, None))
                        con.commit()
                else:
                    with con:
                        cursor = con.cursor()
                        cursor.execute('''
                              INSERT INTO players(id, name, time, score, image_id, curr_img, time_bool, pair, time_score) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                         ''', (id, name, 0, 0, 0, None, False, 0, None))
                        con.commit()


def print_time(id, image_id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time FROM players WHERE id = ? and image_id = ?""", (id, image_id)).fetchall()
    for elem in result:
        return elem


def print_score(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT score FROM players WHERE id = {id}""").fetchall()
    return result


def update_score(id, score):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set score = score + {score} where id = {id}""")
        con.commit()


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


def print_time_bool(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT time_bool FROM players WHERE id = {id}""").fetchall()
    for elem in result:
        return elem[0]


def update_time_bool(id, bool):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, bool)
        cursor.execute(f"""update players set time_bool = '{bool}' where id = {id}""")
        con.commit()


def update_search(id, bool):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, bool)
        cursor.execute(f"""update players set in_searching = {bool} where id = {id}""")
        con.commit()


def print_ready():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = [i[0] for i in cur.execute("""SELECT id FROM players WHERE in_searching = 1""").fetchall()][::-1]
    return result


def print_pair(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT pair FROM players WHERE id = {id}""").fetchall()
    for elem in result:
        return elem[0]


def update_pair(id, id1):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        print(id, id1)
        cursor.execute(f"""update players set pair = {id} where id = {id1}""")
        cursor.execute(f"""update players set pair = {id1} where id = {id}""")
        con.commit()


def clear_pair(id):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set pair = 0 where id = {id}""")
        con.commit()


def print_rating():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT score, name FROM players""").fetchall()
    return sorted(result, key=lambda x: x[0])


def update_suggest_stage(id, stage):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set suggest_stage = {stage} where id = {id}""")
        con.commit()


def print_suggest_stage(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT suggest_stage FROM players where id = {id}""").fetchall()
    return result[0][0]


def print_name(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT name FROM players where id = {id}""").fetchall()
    return result[0][0]


def update_online_imgs(id, imgs):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set online_imgs = '{imgs}' where id = {id}""")
        con.commit()


def print_online_imgs(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT online_imgs FROM players where id = {id}""").fetchall()
    return result[0][0]


def update_online_score(id, score):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set online_score = score + {score} where id = {id}""")
        con.commit()


def print_online_score(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT online_score FROM players where id = {id}""").fetchall()
    return result[0][0]


def update_time_score(id, score):
    con = sqlite3.connect('players.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update players set time_score = time_score + {score} where id = {id}""")
        con.commit()


def print_time_score(id):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT time_score FROM players where id = {id}""").fetchall()
    return result[0][0]

create_table()
