import json
import urllib2


class CommuteServiceClient(object):
    URL = 'http://127.0.0.1:8000/commute'

    def get(self, commute_id):
        if not commute_id:
            return None
        parsed = json.load(urllib2.urlopen("http://127.0.0.1:8000/commute/" + commute_id))
        return json.dumps(parsed, indent=4, sort_keys=True)

    # (location_0, [location_id1,...,location_idn])
    def query(self, commute_query):
        parsed = json.load(urllib2.urlopen(
            url="http://127.0.0.1:8000/commute/bulkGet",
            data=commute_query))
        d = {}
        for c in parsed:
            d[c.seeker_location_id + '-' + c.provider_location_id] = c
        return d


if __name__ == '__main__':
    client = CommuteServiceClient()
    test_location_id = 'fb876c21-1da3-48c4-8761-ced53509f37d'
    json = client.get(test_location_id)
    print(json)
