# Generic single-database configuration with an async dbapi.

---
## Creates a new migration script
```bash
alembic revision --autogenerate -m "Add new table"
```
#### Parameters:
- `-m` or `--message`: A message describing the migration.
- `--autogenerate`: Automatically generate migration scripts based on changes to the database schema.

## Applies migrations to the database
```bash
alembic upgrade head
```
#### Parameters:
- `revision`: Target revision to upgrade to (e.g., `head`, `base`, or a specific revision ID).


## Reverts the database to a previous version
```bash
alembic downgrade -1
```
#### Parameters:
- `revision`: Target revision to downgrade to (e.g., -1 for one step back).


## Displays the current revision of the database
```bash
alembic current
```

## Shows the migration history
```bash
alembic history
```
#### Parameters:
- `--verbose`: Displays additional information about each revision.


## Merges multiple revisions into a single revision
```bash
alembic merge -m "Merge revisions" <revision1> <revision2>
```


## Sets the revision table to a specific revision without applying migrations
```bash
alembic stamp head
```
#### Parameters:
- `revision`: Target revision to stamp (e.g., a specific revision ID)
