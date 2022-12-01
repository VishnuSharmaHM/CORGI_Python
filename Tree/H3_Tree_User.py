from geopy.geocoders import Nominatim
from h3 import h3
from Code import Config as C

def Hex_Value_Address():
    Hex_Parent_C = int(C.config['Obfuscation']['Hex_Parent'])
    geolocator = Nominatim(user_agent="my_user_agent")
    addr=C.config['Obfuscation']['Address']
    loc=geolocator.geocode(addr)
    print(loc)
    h3_address = h3.geo_to_h3(loc.latitude,loc.longitude, Hex_Parent_C)
    out=h3.k_ring_distances(h3_address, 1)

    hex_value=[]
    for i in out:
        for j in i:
            hex_value.append(j)
    hex_value.sort()
    print(hex_value)
    return hex_value