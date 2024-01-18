# Очередность директив docker-compose

1. build/image
2. container_name
3. depends_on
4. restart
5. volumes
6. env_file
7. environment
8. logging
9. healthcheck
10. ports/expose
11. command
12. secrets

# Environments

Правильно:

```yaml
    environment:
      PG_ADMIN_BILLING_DB_HOST: ${PG_ADMIN_BILLING_DB_HOST:-postgres}
      PG_ADMIN_BILLING_DB_PORT: ${PG_ADMIN_BILLING_DB_PORT:-5432}
```

Неправильно:

```yaml
    environment:
      - PG_ADMIN_BILLING_DB_HOST=${PG_ADMIN_BILLING_DB_HOST:-postgres}
      - PG_ADMIN_BILLING_DB_PORT=${PG_ADMIN_BILLING_DB_PORT:-5432}
```