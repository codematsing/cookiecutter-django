# Issues Tracker

* [Need to completely reset database in local development](https://www.linkedin.com/pulse/how-do-i-reset-django-migration-nitin-raturi?trk=pulse-article_more-articles_related-content-card#:~:text=Django%27s%20migration%20can%20be%20reset,and%20python%20manage.py%20migrate.)

```shell
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
# delete and create database
```

Error:
```
django.db.migrations.exceptions.NodeNotFoundError: Migration socialaccount.0001_initial dependencies reference nonexistent parent node ('sites', '0001_initial')

```

Solution:
``` python
# at settings.py
MIGRATION_MODULES = {"sites": "<app_name>.contrib.sites.migrations"} #comment out
```