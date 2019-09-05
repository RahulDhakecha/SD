from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class GeoInfoConn():
    def __init__(self):
        self.geolocator = Nominatim(user_agent="Raj_Group_Dashboard")

    def find_latitude(self, location):
        loc = None
        while loc is None:
            try:
                loc = self.geolocator.geocode(location)
                return loc.latitude
            except AttributeError as ae:
                return None
            except GeocoderTimedOut as ge:
                pass

    def find_longitude(self, location):
        loc = None
        while loc is None:
            try:
                loc = self.geolocator.geocode(location)
                return loc.longitude
            except AttributeError as ae:
                return None
            except GeocoderTimedOut as ge:
                pass


if __name__ == '__main__':
    connection = GeoInfoConn()
    print(connection.find_latitude(location="Surat"))
    print(connection.find_longitude(location="surat"))
