## Run Alembic Migrations

### Configration

```bash
    cp alembic.ini.example alembic.ini
```

- Update the `alembic.ini` with your database credintials (`sqlalchemy.url`)

### (Optional) Create a new migration

```bash
    alembic revision --autogenerate -m "Add....."
```

### upgrade the database

```bash
    alembic upgrade head
```
