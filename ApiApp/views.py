import csv
from io import TextIOWrapper
from typing import Dict, List

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import User
from .serializers import UserSerializer


class CSVUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'detail': 'No file uploaded with key "file".'}, status=status.HTTP_400_BAD_REQUEST)

        if not uploaded_file.name.lower().endswith('.csv'):
            return JsonResponse({'detail': 'Only .csv files are accepted.'}, status=status.HTTP_400_BAD_REQUEST)

        saved_count = 0
        rejected_count = 0
        errors: List[Dict] = []

        text_stream = TextIOWrapper(uploaded_file.file, encoding='utf-8')
        reader = csv.DictReader(text_stream)

        expected_fields = {'name', 'email', 'age'}
        if set([h.strip().lower() for h in reader.fieldnames or []]) != expected_fields:
            return JsonResponse(
                {'detail': 'CSV must contain headers: name,email,age'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_emails = set(User.objects.values_list('email', flat=True))
        seen_emails = set()

        for index, row in enumerate(reader, start=2):  
            raw_name = (row.get('name') or '').strip()
            raw_email = (row.get('email') or '').strip()
            raw_age = (row.get('age') or '').strip()

            email_lower = raw_email.lower()
            if email_lower in existing_emails or email_lower in seen_emails:
                rejected_count += 1
                errors.append({'row': index, 'email': raw_email, 'errors': {'email': ['Duplicate email skipped.']}})
                continue

            age_value = None
            if raw_age != '':
                try:
                    age_value = int(raw_age)
                except ValueError:
                    age_value = raw_age

            serializer = UserSerializer(data={'name': raw_name, 'email': raw_email, 'age': age_value})
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved_count += 1
                    seen_emails.add(email_lower)
                except IntegrityError:
                    rejected_count += 1
                    errors.append({'row': index, 'email': raw_email, 'errors': {'email': ['Duplicate email skipped.']}})
            else:
                rejected_count += 1
                errors.append({'row': index, 'email': raw_email, 'errors': serializer.errors})

        response = {
            'saved': saved_count,
            'rejected': rejected_count,
            'errors': errors,
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
