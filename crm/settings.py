INSTALLED_APPS = [
    'django_crontab',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

INSTALLED_APPS = [
    # existing apps
    'django_celery_beat',
]
