import os
import random
import sqlite3

files = os.listdir('images')

con = sqlite3.connect('images.db')
cur = con.cursor()
id = cur.execute("""select id from images""").fetchall()
coord = str(random.choice(id))[1:-2]

def get_coords():
    return coord


def getImage():
    return coord


def getImages(count):
    return [open(f'images/{i}', 'rb') for i in random.sample(files, count)]

getImage()
