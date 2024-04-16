import os
import random


def getImage():
    files = os.listdir('images')
    print(files)
    return f'images/{random.choice(files)}'


def getImages(count):
    files = os.listdir('images')
    return [f'images/{i}' for i in random.sample(files, count)]
