init:
	tctl auth sign --format=redis --host=localhost --out=single --ttl=2190h
	chmod a+r single*
run:
	docker run -d --name redis -v $(PWD):/opt/redis -p 6379:6379 redis:7.0 redis-server /opt/redis/single.conf

.PHONY: clean
clean: down
	rm -rf single*.crt single*.cas single*.key
