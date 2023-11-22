init:
	tctl auth sign --format=redis --host=10.5.0.5 --out=node0 --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.6 --out=node1 --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.7 --out=node2 --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.8 --out=node3 --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.9 --out=node4 --ttl=2190h
	tctl auth sign --format=redis --host=10.5.0.10 --out=node5 --ttl=2190h
	chmod a+r node*
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
      '    uri: "rediss://10.5.0.10:6379?mode=cluster"'

.PHONY: clean
clean: down
	rm -rf node*.crt node*.cas node*.key
