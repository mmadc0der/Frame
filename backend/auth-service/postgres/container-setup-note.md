# Note for quick setup

**Setup is going to linux containers**

## Linux command

```bash
docker run --name frame-auth-dev-postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=frame \
  -e POSTGRES_DB=frame \
  -v ~/docker-volumes/postgres-data:/var/lib/postgresql/data \
  -v ~/my-migrations:/migrations \
  -p 5430:5432 \
  -d postgres:latest
```

## Windows command

```bash
docker run --name frame-auth-dev-postgres ^
  -e POSTGRES_PASSWORD=mysecretpassword ^
  -e POSTGRES_USER=frame ^
  -e POSTGRES_DB=frame ^
  -v ~/docker-volumes/postgres-data:/var/lib/postgresql/data ^
  -v ~/my-migrations:/migrations ^
  -p 5430:5432 ^
  -d postgres:latest
```