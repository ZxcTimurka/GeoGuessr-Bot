import sqlite3


def create_table():
    con = sqlite3.connect('suggested_images.db')
    with con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS suggested_images(
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        name TEXT,
                        coord_lat FLOAT,
                        coord_long FLOAT
                    )
                ''')


def add_suggested_score(user_id, *coords):
    con = sqlite3.connect('suggested_images.db')
    with con:
        data = con.execute("select count(*) from sqlite_master where type='table' and name='suggested_images'")
        for row in data:
            if row[0] == 0:
                create_table()
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                                        INSERT INTO suggested_images(name, user_id, coord_lat, coord_long) VALUES(?, ?, ?, ?)
                                    ''', ('None', user_id, coords[0], coords[1]))
                    con.commit()
            else:
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                                        INSERT INTO suggested_images(name, user_id, coord_lat, coord_long) VALUES(?, ?, ?, ?)
                                    ''', ('None', user_id, coords[0], coords[1]))
                    con.commit()


def add_photo_name(name, id):
    con = sqlite3.connect('suggested_images.db')
    with con:
        cursor = con.cursor()
        cursor.execute(f"""update suggested_images set name = '{name}' where user_id = {id} and name = 'None'""")
        con.commit()


def print_id(photo_id, name):
    con = sqlite3.connect('suggested_images.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id FROM suggested_images WHERE user_id = {photo_id} and name = """).fetchall()
    return result[0][0]


create_table()
