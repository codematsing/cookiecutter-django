#!/bin/bash
# Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
# To check: ./manage.py showmigrations
#find . \( -path '*/\.*' -prune \) -o \( -path "*/migrations/*.py" -not -name "__init__.py" -print -delete \) -o \( -path "*/migrations/*.pyc" -print -delete \)
find . \( -path '*/\.*' \) -o \( -path "*/migrations/*.py" -not -name "__init__.py" -print -delete \) -o \( -path "*/migrations/*.pyc" -print -delete \)
if [ -f db.sqlite3 ]; then
    rm db.sqlite3
    echo "db.sqlite3 deleted"
fi

# Warning: using this variable may be a concern in security
export PGPASSWORD=$POSTGRES_PASSWORD

dropdb -h localhost -p 5432 -U $POSTGRES_USER $POSTGRES_DB
echo "$POSTGRES_DB deleted"

createdb -h localhost -p 5432 -U $POSTGRES_USER $POSTGRES_DB
echo "$POSTGRES_DB recreated"

echo "You may now reload database from fixtures"

