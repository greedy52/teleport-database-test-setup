VERSION=6.0

init:
	tctl auth sign --format=mongodb --host=localhost --out=mongo --ttl=2190h
	chmod a+r mongo*

up:
	docker run -d --name mongo -p 27017:27017 \
    -v ${PWD}/mongo.cas:/opt/mongo.cas \
    -v ${PWD}/mongo.crt:/opt/mongo.crt \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo:$(VERSION) \
    --wiredTigerCacheSizeGB 1.5 \
    --tlsMode allowTLS \
    --tlsCertificateKeyFile /opt/mongo.crt \
    --tlsCAFile /opt/mongo.cas

down:
	docker rm -f mongo

dump:
	@printf "%s\n" \
      'db_service:' \
      '  enabled: "yes"' \
      '  databases:' \
      '  - name: "self-hosted-mongo"' \
      '    protocol: "mongodb"'\
      '    uri: "localhost:27017"'

dump_autouser:
	@printf "%s\n" \
      'db_service:' \
      '  enabled: "yes"' \
      '  databases:' \
      '  - name: "self-hosted-mongo-auto"' \
      '    protocol: "mongodb"'\
      '    uri: "localhost:27017"' \
      '    static_labels:' \
      '      EnableMongoAutoUser: "true"'\
      '    admin_user:' \
      '      name: "teleport-admin"'

.PHONY: clean
clean: done
	rm mongo.cas mongo.crt
