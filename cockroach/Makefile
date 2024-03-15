VERSION=v23.2.2
up:
	docker run -d \
	--env COCKROACH_DATABASE=test \
	--env COCKROACH_USER=root \
	--env COCKROACH_PASSWORD=password \
  	--name=cockroachdb \
	--hostname=localhost \
    -p 26257:26257 \
    -p 26880:8080 \
  	cockroachdb/cockroach:$(VERSION) start-single-node \
    --http-addr=localhost:8080

root-connect:
	docker exec -it cockroachdb ./cockroach sql --url="postgresql://root@127.0.0.1:26257/defaultdb?sslcert=certs%2Fclient.root.crt&sslkey=certs%2Fclient.root.key&sslmode=verify-full&sslrootcert=certs%2Fca.crt"

root-connect-create-alice:
	docker exec -it cockroachdb ./cockroach sql --url="postgresql://root@127.0.0.1:26257/defaultdb?sslcert=certs%2Fclient.root.crt&sslkey=certs%2Fclient.root.key&sslmode=verify-full&sslrootcert=certs%2Fca.crt" -e "CREATE USER alice WITH PASSWORD NULL;"

copy-certs:
	docker cp cockroachdb:/cockroach/certs/ca.crt cockroach_ca.crt	
	cp cockroach_ca.crt cockroach_ca-client.crt
	tctl auth export --type db-client >> cockroach_ca-client.crt
	docker cp cockroach_ca-client.crt cockroachdb:/cockroach/certs/ca-client.crt
	docker stop cockroachdb
	docker start cockroachdb

dump:
	@printf "%s\n" \
      'db_service:' \
      '  enabled: "yes"' \
      '  databases:' \
      '  - name: "self-hosted-cockroachdb"' \
      '    protocol: "cockroachdb"'\
	  '    uri: "localhost:26257"' \
	  '    tls:'\
	  '    	 mode: verify-ca'\
	  '      ca_cert_file: $(CURDIR)/cockroach_ca.crt'

down:
	docker rm -f cockroachdb

.PHONY: clean
clean: down
	rm -rf server.cas
	rm -rf server.crt
	rm -rf server.key
