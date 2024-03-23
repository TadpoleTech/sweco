import requests
import xmltodict


def query(lon, lat):
    return xmltodict.parse(requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}").content)['reversegeocode']


def city_filter(list_of_posts, cityname):
    '''Returns a dict of posts corrisponging to that city'''
    out = {}
    for post in list_of_posts:
        post_city = query(post["pos_lon"], post["pos_lat"])
        if post_city == cityname:
            out[post["post_id"]] = post
    return out


def suburb_filter(list_of_posts, cityname, suburb_name):
    out = {}
    for post in list_of_posts:
        post_address_data = query(post["pos_lon"], post["pos_lat"])[
            "addressparts"]
        if post_address_data['city'] == cityname and post_address_data['suburb'] == suburb_name:
            out[post["post_id"]] = post
    return out


if __name__ == "__main__":
    area = query(24.938379, 60.169855)
    for key in area["addressparts"]:
        print({key}, {area["addressparts"][key]})
