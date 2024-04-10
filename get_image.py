import os
import random

files = os.listdir('images')


def getImage():
    return f'images/{random.choice(files)}'


def getImages(count):
    return [open(f'images/{i}', 'rb') for i in random.sample(files, count)]
