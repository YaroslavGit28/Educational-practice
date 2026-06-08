from django.test import TestCase, Client


class SmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_page(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
