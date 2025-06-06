SUFFIX ?=
PORT ?= 3306

init:
	tctl auth sign --format=db --host=localhost --out=mysql --ttl=2190h
	bash -c "chown 27:27 mysql.cas"
	bash -c "chown 27:27 mysql.crt"
	bash -c "chown 27:27 mysql.key"

up:
	docker run \
	-e MYSQL_ROOT_PASSWORD=password \
    -v ${PWD}/mysql.cas:/etc/mysql.cas \
    -v ${PWD}/mysql.crt:/etc/mysql.crt \
    -v ${PWD}/mysql.key:/etc/mysql.key \
    -d --name mysql$(SUFFIX) -p $(PORT):3306 \
    mysql/mysql-server:8.0 \
    --bind-address=0.0.0.0 \
    --require_secure_transport=ON \
    --ssl-ca=/etc/mysql.cas \
    --ssl-cert=/etc/mysql.crt \
    --ssl-key=/etc/mysql.key

.PHONY: clean
clean:
	rm -rf mysql.cas
	rm -rf mysql.crt
	rm -rf mysql.key
	docker rm -f mysql
