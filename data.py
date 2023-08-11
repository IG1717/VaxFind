import requests
from requests.structures import CaseInsensitiveDict
import json
from geopy.geocoders import Nominatim


def get_title(address, index):
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(address)

    print(loc.latitude,loc.longitude)
    lat = str(loc.latitude)
    longi = str(loc.longitude)

    url = "https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat=" + lat + "&long=" + longi + "&radius=10"

    headers = CaseInsensitiveDict()
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept"] = "*/*"
    headers["Accept-Language"] = "en-us"
    headers["Host"] = "api.us.castlighthealth.com"
    headers["User-Agent"] = "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)"

    resp = requests.get(url, headers=headers)
    response = json.loads(resp.content)

    stock = response['providers'][index]['in_stock']

    if stock != True:
        index = index + 1 

    name = response['providers'][index]['name']

    address1 = response['providers'][index]['address1']
    city = response['providers'][index]['city']
    state = response['providers'][index]['state']
    zip_code = response['providers'][index]['zip']

    location = (address1 + ", " + city + ", " + state + ", " + zip_code)



    print("Location: " + name + " In Stock: " + str(stock))
    return name + ", " + location

def get_location_data(id):
    url = "https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/" + id

    headers = CaseInsensitiveDict()
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept"] = "*/*"
    headers["Accept-Language"] = "en-us"
    headers["Host"] = "api.us.castlighthealth.com"
    headers["User-Agent"] = "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)"

    resp = requests.get(url, headers=headers)
    response = json.loads(resp.content)

    name = response['website']
    return name

print(get_location_data("5b4807ed-f8a3-43c3-a671-574f99f72205"))