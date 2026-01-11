# CRM Celery Report Setup

## Requirements
- Redis
- Python dependencies

## Installation Steps

1. Install Redis
   - Ubuntu: sudo apt install redis-server
   - macOS: brew install redis

2. Install Python dependencies
   pip install -r requirements.txt

3. Run migrations
   python manage.py migrate
   python manage.py migrate django_celery_beat

4. Start Redis
   redis-server

5. Start Celery Worker
   celery -A crm worker -l info

6. Start Celery Beat
   celery -A crm beat -l info

7. Verify Logs
   Check the report output in:
   /tmp/crm_report_log.txt
