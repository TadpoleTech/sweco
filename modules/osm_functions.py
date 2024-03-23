import requests
import xmltodict


def query(lon, lat):
    return xmltodict.parse(requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}").content)['reversegeocode']


if __name__ == "__main__":
    area = query(24.938379, 60.169855)
    for key in area["addressparts"]:
        print({key}, {area["addressparts"][key]})
