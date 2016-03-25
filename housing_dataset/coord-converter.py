import pandas as pd
from geopy.geocoders import Nominatim
import geocoder
import time

USAGE_LIMIT = 10 # Requests per second

def convert_address(address):
    time.sleep(1/USAGE_LIMIT)
    location = geocoder.google(address)
    return location.lat, location.lng

print("\rReading CSV file.")
data = pd.read_csv("PublishAffordableExcel.csv")
print("\rConverting addresses.")
data['lat'], data['lng'] = zip(*data["Address"].map(convert_address))
print("\rWriting CSV file.")
data.to_csv("PublishAffordableCoordinate.csv")
