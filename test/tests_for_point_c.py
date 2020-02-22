import unittest
from juan.point_c.cache.executor import app as cache_app
from juan.point_c.router.executor import app as router_app

import json
from urllib.parse import urlencode


class CacheTests(unittest.TestCase):

    def setUp(self):
        cache_app.config['TESTING'] = True
        self.cache_app = cache_app.test_client()
        router_app.config['TESTING'] = True
        self.router_app = router_app.test_client()

    def test_get_status(self):
        expected_response_body = b'{"db":"connected","lat_long":"25.759557,' \
                                 b'-80.374231","region":"florida","version":"0.1"}\n'

        response = self.cache_app.get('/v1/caches/status')

        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(expected_response_body, response.data)

    def test_post(self):
        headers = {'Content-Type': 'application/json', 'X-Key': 'juan'}
        response = self.cache_app.post('/v1/caches', headers=headers, data=json.dumps({'name': 'juan', 'id': '1000'}))
        self.assertEqual(response.status, '201 CREATED')

        response = self.cache_app.post('/v1/caches', headers={}, data=json.dumps({'name': 'juan', 'id': '1000'}))
        self.assertEqual(response.status, '422 UNPROCESSABLE ENTITY')
        self.assertEqual(response.json['payload']['error'], 'AssertionError')

    def test_get(self):
        response = self.cache_app.get('/v1/caches/somekey')
        self.assertEqual(response.status, '404 NOT FOUND')
        response = self.cache_app.get('/v1/caches/juan')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.data, b'{"name": "juan", "id": "1000"}')


class RouterTests(unittest.TestCase):

    def setUp(self):
        router_app.config['TESTING'] = True
        self.router_app = router_app.test_client()

    def test_post(self):
        headers = {'Content-Type': 'application/json'}
        body = {'region': 'AU', 'lat': '-37.810745', 'long': '144.965207', 'url': 'http://au.mycompany.com/v1/caches'}
        response = self.router_app.post('/v1/routes', headers=headers, data=json.dumps(body))
        self.assertEqual(response.status, '201 CREATED')

        body = {'region': 'USA', 'lat': '37.755879', 'long': '-122.482184', 'url': 'http://usa.mycompany.com/v1/caches'}
        response = self.router_app.post('/v1/routes', headers=headers, data=json.dumps(body))
        self.assertEqual(response.status, '201 CREATED')

        response = self.router_app.post('/v1/routes', headers=headers, data=json.dumps({'region': 'Latam'}))
        self.assertEqual(response.status, '422 UNPROCESSABLE ENTITY')
        self.assertEqual(response.json['payload']['error'], 'AssertionError')

    def test_get(self):
        response = self.router_app.get('/v1/routes?{}'.format(urlencode({'lat': '38.561387', 'long': '-121.498287'})))
        self.assertEqual(response.json['region'], 'USA')

        response = self.router_app.get('/v1/routes?{}'.format(urlencode({'lat': '-34.929826',
                                                                         'long': '138.591034',
                                                                         'radius': '700'})))
        self.assertEqual(response.json['region'], 'AU')

        response = self.router_app.get('/v1/routes?{}'.format(urlencode({'lat': '-34.929826',
                                                                         'long': '138.591034',
                                                                         'radius': '550'})))
        self.assertEqual(response.status, '404 NOT FOUND')


if __name__ == "__main__":
    unittest.main()
