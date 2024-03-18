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
    if round(distance * 1.609344, 2) < 0.05:
        return 'Поздравляем, у вас получилось!'
    if round(distance * 1.609344, 2) < 1:
        return f'{round(distance * 1.609344, 2) / 1000} м'
    return f'{round(distance * 1.609344, 2)} км'
