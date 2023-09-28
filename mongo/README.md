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
