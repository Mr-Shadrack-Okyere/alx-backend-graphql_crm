#!/bin/bash

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED_COUNT=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

echo \"[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
