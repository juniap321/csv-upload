Project: DRF CSV Upload API

Overview
This Django REST Framework API provides a POST endpoint to upload a CSV file containing user data and saves valid records to the database.

Endpoint
- URL: /upload-csv/
- Method: POST
- Content-Type: multipart/form-data
- Form field: file (must be a .csv)

CSV Format
Headers (exact, lowercase): name,email,age
Example rows:
Alice,alice@example.com,25
Bob,bob@example.com,40

Validation Rules
- name: non-empty string
- email: valid email
- age: integer, 0-120
- duplicate emails: gracefully skipped (existing in DB or repeated in the same file)

Response
{
  "saved": 2,
  "rejected": 1,
  "errors": [
    {"row": 4, "email": "alice@example.com", "errors": {"email": ["Duplicate email skipped."]}}
  ]
}

Local Setup
1) Install dependencies
   pip install django==5.0.10 djangorestframework==3.15.2
2) Apply migrations
   python manage.py migrate
3) Run server
   python manage.py runserver

Test the API
Using curl:
curl -X POST http://127.0.0.1:8000/upload-csv/ \
  -F "file=@samples/users_sample.csv"

Run unit tests:
python manage.py test ApiApp

Project Structure (key files)
- ApiApp/models.py: User model
- ApiApp/serializers.py: User serializer with validations
- ApiApp/views.py: CSV upload view
- ApiApp/urls.py: App routes
- API/urls.py: Project routes including ApiApp
- samples/users_sample.csv: Sample input CSV
- samples/sample_response.json: Example API response

Notes
- Only .csv files are accepted.
- Email field is unique; duplicates are skipped without raising server errors.

