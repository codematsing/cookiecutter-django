#!/bin/bash
# Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
# To check: ./manage.py showmigrations
#find . \( -path '*/\.*' -prune \) -o \( -path "*/migrations/*.py" -not -name "__init__.py" -print -delete \) -o \( -path "*/migrations/*.pyc" -print -delete \)
find . \( -path '*/\.*' \) -o \( -path "*/migrations/*.py" -not -name "__init__.py" -print -delete \) -o \( -path "*/migrations/*.pyc" -print -delete \)
if [ -f db.sqlite3 ]; then
    rm db.sqlite3
    echo "db.sqlite3 deleted"
fi

if sudo psql -lqt | cut -d \| -f 1 | grep -qw $(POSTGRES_DB); then
    sudo dropdb $(POSTGRES_DB)
    echo "$(POSTGRES_DB) deleted"
fi

sudo createdb $(POSTGRES_DB)
echo "$(POSTGRES_DB) recreated"

echo "You may now reload database from fixtures"
