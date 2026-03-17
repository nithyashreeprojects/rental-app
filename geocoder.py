import requests
import os
from dotenv import load_dotenv
from math import radians,sin,cos,sqrt,atan2

load_dotenv()

API_KEY=os.getenv("OPENCAGE_API_KEY")

def get_coordinates(area,city):
    query=f"{area}, {city}, India"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={API_KEY}&limit=1"
    response = requests.get(url)
    data = response.json()

    if data["total_results"]>0:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        return lat,lng

    return None, None

def haversine(lat1,lng1,lat2,lng2):
    R = 6371 # earth's radius in kilometers
    lat1,lng1,lat2,lng2 = map(radians,[lat1,lng1,lat2,lng2 ])
    dlat = lat2-lat1
    dlng = lng2 -lng1

    a = sin(dlat/2)**2 +cos(lat1)*cos(lat2) *sin(dlng/2)**2
    c = 2* atan2(sqrt(a),sqrt(1-a))
    return round(R*c,2)

def get_proximity_score(tenant_area,tenant_city,property_area,property_city):
    if tenant_area.strip() == "":
        return 10
    lat1,lng1 = get_coordinates(tenant_area,tenant_city)
    lat2,lng2 = get_coordinates(property_area,property_city)

    if lat1 is None or lat2 in None:
        return 5
    
    distance = haversine(lat1,lng1,lat2,lng2)

    if distance <= 3:
        return 20
    elif distance <=7:
        return 15
    elif distance <=15:
        return 8
    else:
        return 2
