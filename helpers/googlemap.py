import googlemaps

class GoogleMapSearch:
    def __init__(self, location, radius):
        self._gmaps = googlemaps.Client(key="AIzaSyDwkIdBAYF1JV8ctI3Gp2ZId6R8NP44tKc")
        self._location = location
        self._radius = radius
        self.result = []
    
    def get_info(self):
        search_result = self._gmaps.places_nearby(self._location, self._radius, type="restaurant", language="zh-TW")
        
        for place in search_result['results']:
            data = {}
            data['name'] = place['name']
            # print(place)
            data['location'] = place['geometry']['location']
            data['photo'] = self.get_photo(place['photos'][0]['photo_reference'])
            data['rating'] = place['rating']
            self.result.append(data)
        return self.result
        # self.result = pd.DataFrame.from_dict(self.result)

    def get_photo(self, photo_reference):
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key=AIzaSyDwkIdBAYF1JV8ctI3Gp2ZId6R8NP44tKc"
        