from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User


class CSVUploadAPITests(TestCase):
    def test_reject_non_csv(self):
        url = reverse('upload-csv')
        file = SimpleUploadedFile('data.txt', b'name,email,age\nJohn,john@example.com,30\n')
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, 400)

    def test_upload_and_skip_duplicates(self):
        url = reverse('upload-csv')
        csv_content = (
            'name,email,age\n'
            'Alice,alice@example.com,25\n'
            'Bob,bob@example.com,40\n'
            'Alice Dup,alice@example.com,26\n'  # duplicate
        ).encode('utf-8')
        file = SimpleUploadedFile('users.csv', csv_content, content_type='text/csv')
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['saved'], 2)
        self.assertEqual(data['rejected'], 1)
        self.assertEqual(User.objects.count(), 2)

    def test_validation_errors(self):
        url = reverse('upload-csv')
        csv_content = (
            'name,email,age\n'
            ',bademail,130\n'
        ).encode('utf-8')
        file = SimpleUploadedFile('users.csv', csv_content, content_type='text/csv')
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['saved'], 0)
        self.assertEqual(data['rejected'], 1)
        self.assertTrue(len(data['errors']) == 1)
from django.test import TestCase

# Create your tests here.
