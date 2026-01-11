INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_crontab",

    "graphene_django",  # Add graphene-django
    "crm",              # Add your crm app
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema",  # Path to your schema
}
