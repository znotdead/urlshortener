from urllib.parse import urljoin
from unittest.mock import patch

from django.test import Client
from snapshottest.django import TestCase
from graphene.test import Client as GraphClient

from .schema import schema
from .models import ShortURL


class GetShortURL(TestCase):

    def setUp(self):
        self.gc = GraphClient(schema)

    def test_get_url_by_code(self):
        shorturl = ShortURL(code="abc", long_url="http://localhost:8000/")
        shorturl.save()
        self.assertMatchSnapshot(self.gc.execute('''
            {
                exist: getShorturl(code: "abc") {
                    longUrl
                }
            }
            '''))

    def test_get_url_by_nonexists_code(self):
        self.assertMatchSnapshot(self.gc.execute('''
            {
                nonexist: getShorturl(code: "NONEXISTS") {
                    longUrl
                }
            }
            '''))


class CreateShortURL(TestCase):

    def setUp(self):
        self.gc = GraphClient(schema)

    def create_shortenurl(self, long_url):
        request = '''
            mutation {{
                createShorturl(longUrl: "{0}") {{
                    shorturl {{
                        longUrl
                        code
                    }}
                    ok
                    urlWithCode
                }}
            }}'''.format(long_url)
        return self.gc.execute(request)

    def test_create(self):
        long_url = "http://localhost/"
        created = self.create_shortenurl(long_url)
        self.assertEqual(len(ShortURL.objects.all()), 1)
        shorturl = ShortURL.objects.first()
        self.assertEqual(created, {
            'data': {
                'createShorturl': {
                    'ok': True,
                    'shorturl': {
                        'code': shorturl.code,
                        'longUrl': long_url
                    },
                    'urlWithCode': 'http://localhost/{}'.format(shorturl.code)
                }}})

        result = self.gc.execute('''
            {{
                exist: getShorturl(code: "{0}") {{
                    longUrl
                }}
            }}
            '''.format(shorturl.code))
        self.assertEqual(result, {'data': {'exist': {'longUrl': long_url}}})

    def test_create_with_invalid_URL(self):
        long_url = "a"*300
        created = self.create_shortenurl(long_url)
        self.assertEqual(len(ShortURL.objects.all()), 0)


class ShortURLTestCase(TestCase):

    def setUp(self):
        self.c = Client()

    def test_save_same_code_shorturl(self):
        shorturl1 = ShortURL(code='exists', long_url='url1')
        shorturl1.save()
        with patch.object(ShortURL, 'generate_code') as mock_class:
            mock_class.side_effect = ('exists', 'nonexists')
            shorturl2 = ShortURL(long_url='url2')
            shorturl2.save()
        self.assertNotEqual(shorturl1.code, shorturl2.code)

    def test_redirect_shorturl(self):
        long_url = 'http://test_long_url'
        local_url = 'http://localhost:8000/'
        code = 'abc'
        shorturl = ShortURL(code=code, long_url=long_url)
        shorturl.save()
        response = self.c.get(urljoin(local_url, code)+'/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, long_url, fetch_redirect_response=False)

    def test_404(self):
        code = 'noexists'
        local_url = 'http://localhost:8000/'
        response = self.c.get(urljoin(local_url, code)+'/')
        self.assertEqual(response.status_code, 404)
