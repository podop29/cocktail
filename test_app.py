from app import app
from unittest import TestCase

class HomePageTestCase(TestCase):
    def test_home_load(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<h3 class="center">Find your new favorite drink</h3>',html)
    
    def test_home_post(self):
        with app.test_client() as client:
            res = client.post('/',
                                data={'name': 'long island',
                                    'choice': 'drinks'})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)

