import json
import urllib2
import os

class LocationServiceClient:

    DEFAULT_URL = os.getenv('USER_SVC_URL', 'http://127.0.0.1:8012/location/');

    def __init__(self, url):
        if url:
            self.url = url
        else:
            self.url = DEFAULT_URL

    def get(self, ids):
        if not ids:
            return [];
        parsed = json.loads(urllib2.urlopen(self.url + 'search?ids=' + ",".join(ids)))
        return parsed

if __name__ == '__main__':
    client = LocationServiceClient();
    test_ids = ['fb876c21-1da3-48c4-8761-ced53509f37d']
    obj = client.get(test_ids)
    print(json.dumps(obj)