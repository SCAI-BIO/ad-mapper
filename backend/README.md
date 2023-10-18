

## For Database migration check: https://www.educative.io/answers/how-to-use-postgresql-database-in-fastapi
To create a migration version:
- alembic revision --autogenerate -m "New Migration"
- Then go to the revision file and copy the revision id
- Run alembic upgrade <revision_id> 
