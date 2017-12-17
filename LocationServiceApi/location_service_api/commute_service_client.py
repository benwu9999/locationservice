import json
import urllib2

import os


class CommuteServiceClient(object):
    DEFAULT_URL = os.getenv('USER_SVC_URL', 'http://127.0.0.1:8012/commute/')
    content_type = {'Content-Type': 'application/json'}

    def __init__(self, url):
        if url:
            self.url = url
        else:
            self.url = CommuteServiceClient.DEFAULT_URL

    def get(self, ids):
        if not ids:
            return [];
        parsed = json.loads(urllib2.urlopen(self.url + 'commute'))
        return parsed

    def query_pair(self, commute_query):
        """
        :param commute_query: [(user_location_id1, job_post_location_id1),...]
        :return: list of commute_info in the order of input [commuter_info1, ...]
        """
        json_text = json.dumps(commute_query)
        req = urllib2.Request(self.url + 'bulkGetPair', json_text, self.content_type)
        response = urllib2.urlopen(req)
        result = response.read()
        parsed = json.loads(result)
        return parsed


def test_get_ids():
    test_ids = ['fb876c21-1da3-48c4-8761-ced53509f37d']
    obj = client.get(test_ids)
    print(json.dumps(obj))


if __name__ == '__main__':
    client = CommuteServiceClient(None)
    # test_get_ids()
    location_id_pairs = {'8f6f80b6ac9849b2a9a2c846eeb43f2a': ['6d34948c08614237899fc26d899ec6db']}
    # location_id_pairs = {'8f6f80b6': ['6d34948c08614237899fc26d899ec6db']}
    obj = client.query_pair(location_id_pairs)
    print(json.dumps(obj))
