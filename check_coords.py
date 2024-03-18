import requests


def check(coords_orig, coords_app):
    #print(coords_orig, coords_app)
    orig_request = f"http://static-maps.yandex.ru/1.x/?pt={coords_app[1]},{coords_app[0]},pmgrs2~{coords_orig[1]},{coords_orig[0]},pmgrs1&pl={coords_app[1]},{coords_app[0]},{coords_orig[1]},{coords_orig[0]}&l=map"
    orig_response = requests.get(orig_request)
    if not orig_response:
        return 'Ошибка'
    orig_map = 'orig_map.jpeg'
    with open(orig_map, "wb") as file:
        file.write(orig_response.content)
    return open(orig_map, "rb")