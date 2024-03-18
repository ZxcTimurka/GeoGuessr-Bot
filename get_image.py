import os
import random

files = os.listdir('images')


def getImage():
    return open(f'images/{random.choice(files)}', 'rb')


def getImages(count):
    return [open(f'images/{i}', 'rb') for i in random.sample(files, count)]
