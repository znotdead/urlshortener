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
        long_url = "http://sdfeter"
        created = self.create_shortenurl(long_url)
        self.assertEqual(len(ShortURL.objects.all()), 1)
        shorturl = ShortURL.objects.first()
        self.assertEqual(created,
            {'data': {
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
        self.assertEqual(result, 
            {'data': {'exist': {'longUrl': long_url}}})
                
    def test_create_with_invalid_URL(self):
        long_url = "a"*300
        created = self.create_shortenurl(long_url)
        print(created)
        shorturl = ShortURL.objects.first()
        print(shorturl.code, shorturl.long_url)
        self.assertEqual(len(ShortURL.objects.all()), 0)




   # def _test_create_shorturl(self):
   #     c = Client()
   #     long_url = 'http://localhost:8000/'
   #     response = c.post('/shorten/', {'long_url': long_url})
   #     self.assertEqual(response.status_code, 200)
