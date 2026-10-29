from django.test import TestCase, Client
from django.urls import reverse

class PDFConverterTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_convert_no_images(self):
        response = self.client.post(reverse('convert_images'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())