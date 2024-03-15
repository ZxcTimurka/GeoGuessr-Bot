import requests


def check(coords_orig, coords_app):
    orig_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_orig[0]},{coords_orig[1]}&spn=10,10&l=map"
    app_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_app[0]},{coords_app[1]}&spn=10,10&l=map"
    orig_response = response = requests.get(orig_request)
    app_response = response = requests.get(app_request)
    if not orig_response or not app_response:
        return 'Ошибка'
    orig_map = 'orig_map.jpeg'
    app_map = 'app_map.jpeg'
    orig_file = open(orig_map, "wb")
    with open(orig_map, "wb") as file:
        file.write(response.content)
    with open(app_map, "wb") as file:
        file.write(response.content)
    return open(orig_map, "r"), open(app_map, "r")