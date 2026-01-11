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

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generatecrmreport',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
