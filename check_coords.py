import requests


def check(coords_orig, coords_app):
    orig_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_orig[0]},{coords_orig[1]}&spn=85.016233,56.483675&l=map"
    app_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_app[0]},{coords_app[1]}&spn=85.016233,56.483675&l=map"
    orig_response = response = requests.get(orig_request)
    app_response = response = requests.get(app_request)
    if not orig_response or not app_response:
        return 'Ошибка'
    map_file = 'map_file'
    with open(map_file, "wb") as file:
        file.write(response.content)
    with open(map_file, "wb") as file:
        file.write(response.content)