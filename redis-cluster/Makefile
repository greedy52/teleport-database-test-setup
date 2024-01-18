copy-conf:
	mkdir -p node0
	mkdir -p node1
	mkdir -p node2
	mkdir -p node3
	mkdir -p node4
	mkdir -p node5
	cp redis.conf node0/
	cp redis.conf node1/
	cp redis.conf node2/
	cp redis.conf node3/
	cp redis.conf node4/
	cp redis.conf node5/
	cp users.acl node0/
	cp users.acl node1/
	cp users.acl node2/
	cp users.acl node3/
	cp users.acl node4/
	cp users.acl node5/
init: copy-conf
	tctl auth sign --format=redis --host=10.5.0.5 --out=node0/node --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.6 --out=node1/node --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.7 --out=node2/node --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.8 --out=node3/node --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.9 --out=node4/node --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.10 --out=node5/node --ttl=2190h
	chmod a+r node*/*
up:
	docker-compose up -d
down:
	docker-compose down

dump:
	@printf "%s\n" \
      'db_service:' \
      '  enabled: "yes"' \
      '  databases:' \
      '  - name: "self-hosted-redis-cluster"' \
      '    protocol: "redis"'\
      '    uri: "rediss://10.5.0.10:7001?mode=cluster"'

.PHONY: clean
clean: down
	rm -rf node*.crt node*.cas node*.key
