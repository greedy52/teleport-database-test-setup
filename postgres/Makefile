VERSION=16
PORT=5432
NAME=postgres

init:
	tctl auth sign --format=db --host=localhost --out=server --ttl=2190h
	bash -c "chown 999:999 server.cas"
	bash -c "chown 999:999 server.crt"
	bash -c "chown 999:999 server.key"

up:
	docker run \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=password \
	-e POSTGRES_DB=test \
    -v ${PWD}/pg_hba.conf:/opt/postgres/pg_hba.conf \
    -v ${PWD}/server.cas:/opt/postgres/server.cas \
    -v ${PWD}/server.crt:/opt/postgres/server.crt \
    -v ${PWD}/server.key:/opt/postgres/server.key \
    -v ${PWD}/initdb.sh:/docker-entrypoint-initdb.d/config_hba.sh \
    -v ${PWD}/initdb.sql:/docker-entrypoint-initdb.d/setup.sql \
	-d --name $(NAME) -p $(PORT):5432 \
    postgres:$(VERSION) \
	-c "ssl=on" \
	-c "ssl_cert_file=/opt/postgres/server.crt" \
	-c "ssl_key_file=/opt/postgres/server.key" \
	-c "ssl_ca_file=/opt/postgres/server.cas"

.PHONY: clean
clean:
	rm -rf server.cas
	rm -rf server.crt
	rm -rf server.key
	docker rm -f postgres
