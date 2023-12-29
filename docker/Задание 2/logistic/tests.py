from django.test import TestCase
from rest_framework.test import APIClient


class TestSomething(TestCase):
    def test_ok(self):
        client = APIClient()
        response = client.get('/api/v2/')
        assert response.status_code == 200
