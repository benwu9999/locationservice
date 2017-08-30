import json
import urllib2


class CommuteServiceClient(object):
    DEFAULT_URL = os.getenv('USER_SVC_URL', 'http://127.0.0.1:8012/commute/')

    def get(self, ids):
        if not ids:
            return [];
        parsed = json.loads(urllib2.urlopen(self.url + 'search?ids=' + ",".join(ids)))
        return parsed

    # (location_0, [location_id1,...,location_idn])
    def query(self, commute_query):
        parsed = json.load(urllib2.urlopen(self.url, data=commute_query))
        d = {}
        for c in parsed:
            d[c.seeker_location_id + '-' + c.provider_location_id] = c
        return d


if __name__ == '__main__':
    client = CommuteServiceClient()
    test_ids = ['fb876c21-1da3-48c4-8761-ced53509f37d']
    obj = client.get(test_ids)
    print(json.dumps(obj)