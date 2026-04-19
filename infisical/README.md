# Infisical

Trial self-hosted Infisical stack for internal use on `docker-01`.

## Notes

- Routed through Traefik at `https://infisical.openshaw.tech`
- Uses a stack-local Postgres and Redis for simple testing and rollback
- Secrets live in `.env`, which is intentionally not committed
- If this becomes long-lived infrastructure, move it to a dedicated VM and
  consider separating the database lifecycle from the app stack
