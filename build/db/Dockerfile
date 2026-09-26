# MariaDB with rAthena's SQL baked in: a new, empty database volume is initialized
# automatically on first start, so the VM doesn't need the rAthena source.
FROM mariadb:noble
COPY sql-files/*.sql /docker-entrypoint-initdb.d/
