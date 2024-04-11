import sqlite3


def create_table():
    con = sqlite3.connect('images.db')
    with con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS images(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        coord_lat FLOAT,
                        coord_long FLOAT
                    )
                ''')


def add_location(name, coord0, coord1):
    con = sqlite3.connect('images.db')
    with con:
        data = con.execute("select count(*) from sqlite_master where type='table' and name='images'")
        for row in data:
            if row[0] == 0:
                create_table()
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                                    INSERT INTO images(name, coord_lat, coord_long) VALUES(?, ?, ?)
                                ''', (name, coord0, coord1))
                    con.commit()
            else:
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                                    INSERT INTO images(name, coord_lat, coord_long) VALUES(?, ?, ?)
                                ''', (name, coord0, coord1))
                    con.commit()


def search_by_coords(coords0, coords1):
    con = sqlite3.connect('images.db')
    cur = con.cursor()
    result = cur.execute("""select name from images where coord_lat = ? and coord_long = ?""",
                         (coords0, coords1)).fetchall()
    for elem in result:
        return elem


def search_by_id(id):
    con = sqlite3.connect('images.db')
    cur = con.cursor()
    result = cur.execute("""select coord_lat, coord_long from images where id = ?""",
                         (id,)).fetchall()
    for elem in result:
        return elem


def next_id():
    con = sqlite3.connect('images.db')
    cur = con.cursor()
    result = cur.execute("""select id from images""").fetchall()
    return max(result)[0] + 1