from geopy.geocoders import Nominatim
import requests


def search_places(keyword, limit=5):
    geolocator = Nominatim(user_agent="my_geocoder")  # Provide a custom user agent
    locations = geolocator.geocode(keyword, exactly_one=False, limit=limit)

    result = []
    for item in locations:
        result.append({
            'place_id': item.raw['place_id'],
            'osm_id': item.raw['osm_id'],
            'lat': item.latitude,
            'lon': item.longitude,
            'address': item.address,
        })
    return result


def get_addresses_by_keyword(keyword, limit=5):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": keyword,
        "format": "json",
        "limit": limit
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception('Error: '+{response.status_code})

    result = []
    for item in response.json():
        result.append({
            'place_id':item['place_id'],
            'osm_id':item['osm_id'],
            'lat':item['lat'],
            'lon':item['lon'],
            'display_name':item['display_name'],
        })
    return result