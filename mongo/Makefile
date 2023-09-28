init:
	tctl auth sign --format=mongodb --host=localhost --out=mongo --ttl=2190h
	chmod a+r mongo*

up:
	docker run -d --name mongo -p 27017:27017 \
    -v ${PWD}/mongo.cas:/opt/mongo.cas \
    -v ${PWD}/mongo.crt:/opt/mongo.crt \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo:6.0 \
    --wiredTigerCacheSizeGB 1.5 \
    --tlsMode allowTLS \
    --tlsCertificateKeyFile /opt/mongo.crt \
    --tlsCAFile /opt/mongo.cas

clean:
	docker rm -f mongo
	rm mongo.cas mongo.crt
