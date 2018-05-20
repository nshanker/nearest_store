import urllib, json
from pymorton import interleave_latlng
from math import sqrt, radians, sin, cos, asin

def convert_to_1D(location):
    ''' Map any store address to a single number! '''

    if location.has_key('address'):
        formatted_address, lat, lon = geo(location['address'])
        lat = float(lat)
        lon = float(lon)
    elif location.has_key('lat') and location.has_key('lon'):
        lat = float(location['lat'])
        lon = float(location['lon'])
    else:
        return None

    # Next, convert lat and long each into a positive int.
    code = interleave_latlng(lat, lon)

    # Now, turn the lat/long pair into a single number
    if location.has_key('address'):
        return { 'id' : code, 'lat' : lat, 'lon' : lon }
    else:
        return code

def geo(query):
    ''' Use Google Geocoding API to geocode address into lat/long 
        NOTE: The API Key used here is for Shanker's personal use 
    '''

    base = 'https://maps.googleapis.com/maps/api/geocode/json?'
    location = 'address=' + query.replace(' ', '+')     # The same query works for both address and zip

    url = base + location + '&key=' + 'AIzaSyCiN8qhbkFi59wKGP8yvuR1pXwmzHtGsjc'

    response = urllib.urlopen(url)
    data = json.loads(response.read())

    if data['status'] == 'OK':
        result = data['results'][0]
        return (result['formatted_address'], result['geometry']['location']['lat'], result['geometry']['location']['lng'])
    else:
        return (None, None, None)

def haversine(lat1, long1, lat2, long2, units='mi'):
    ''' Find the 'as-the-crow-flies' geodetic distance between two points 
        on earth. The radius of earth is taken to be 6371 km. 
        This formula is taken from a post on stackoverflow.com. It accounts 
        for the earth's curvature and gives good results for small
        distances and large distances alike.
    '''

    lat1, long1, lat2, long2 = map(radians, map(float, [lat1, long1, lat2, long2]))
    dlon = long2 - long1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    if units == 'km':
        r = 6371
    else:
        r = 3956    # earth's radius in miles

    return c * r
