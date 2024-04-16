from numpy import sin, cos, arccos, pi, round


def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees


def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians


def getDistance(latitude1, longitude1, latitude2, longitude2):
    theta = longitude1 - longitude2
    distance = 60 * 1.1515 * rad2deg(arccos((sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + (
                cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))))
    result = round(distance * 1.609344, 2)
    if result <= 1:
        result *= 100
        return int(round((100 - result) / 10)), f'{result}' 'м'
    return 0, 'Ты не угадал🥺'
