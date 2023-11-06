1. `make init`
2. `make up`
3. `docker exec -it mongo mongosh -u mongoadmin -p secret`, then
```
db.getSiblingDB("$external").runCommand(
  {
    createUser: "CN=alice",
    roles: [
      { role: "readWriteAnyDatabase", db: "admin" }
    ]
  }
)
```

Note use `docker exec -it mongo mongo -u mongoadmin -p secret` if `mongosh`
does not exist.

Use `Makefile_4.0` for Mongo v4.0.
