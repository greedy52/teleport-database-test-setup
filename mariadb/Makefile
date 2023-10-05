VERSION=10.9

init:
	tctl auth sign --format=db --host=localhost --out=mariadb --ttl=2190h
	bash -c "chown 999:999 mariadb.cas"
	bash -c "chown 999:999 mariadb.crt"
	bash -c "chown 999:999 mariadb.key"

up:
	docker run \
    -e MYSQL_ROOT_PASSWORD=password \
    -e MARIADB_ROOT_PASSWORD=password \
    -v ${PWD}/mariadb.cas:/etc/mariadb.cas \
    -v ${PWD}/mariadb.crt:/etc/mariadb.crt \
    -v ${PWD}/mariadb.key:/etc/mariadb.key \
    -d --name mariadb -p 3307:3306 \
	mariadb:$(VERSION) \
    --bind-address=0.0.0.0 \
    --ssl-ca=/etc/mariadb.cas \
    --ssl-cert=/etc/mariadb.crt \
    --ssl-key=/etc/mariadb.key

down:
	docker rm -f mariadb

.PHONY: clean
clean: done
	rm -rf mariadb.cas
	rm -rf mariadb.crt
	rm -rf mariadb.key
