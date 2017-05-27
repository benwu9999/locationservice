import json
import urllib2
import os

class LocationServiceClient:

    URL = os.getenv('APPLICATION_SVC_URL', 'http://127.0.0.1:8000/location/');

    def get(self, location_id):
        if not location_id:
            return None;
        parsed = json.load(urllib2.urlopen(self.URL + location_id))
        return json.dumps(parsed, indent=4, sort_keys=True)

    def get_ids(self):
        pass

if __name__ == '__main__':
    client = LocationServiceClient();
    test_id = 'fb876c21-1da3-48c4-8761-ced53509f37d'
    json = client.get(test_id)
    print(json)
