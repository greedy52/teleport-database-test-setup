
Setup
```
make init
make up
docker exec -it mariadb sh
mysql -uroot -p
``` 
(Tip 1: `root` password is `password`.)
(Tip 2: use `mariadb` instead `mysql` for MariaDB 11)

Database Service:
```
db_service:
  enabled: "yes"
  databases:
  - name: "self-hosted-mariadb"
    protocol: "mysql"
    uri: "localhost:3307"
```
