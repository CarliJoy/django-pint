psql -c "create database django_pint;" -U postgres
# Settings done according to tutorial https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
# Please not you might have to edit your pg_hba.conf in your local installation
# see https://docs.boundlessgeo.com/suite/1.1.1/dataadmin/pgGettingStarted/firstconnect.html#allowing-local-connections
psql -c "CREATE USER django_pint WITH PASSWORD 'not_secure_in_testing';" -U postgres
psql -c "ALTER ROLE django_pint SET client_encoding TO 'utf8';" -U postgres
psql -c "ALTER ROLE django_pint SET timezone TO 'UTC';" -U postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE django_pint TO django_pint;" -U postgres
psql -c "ALTER ROLE django_pint CREATEDB;" -U postgres
