self-signed:
	openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes -keyout self-signed.key -out self-signed.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP.1:10.5.0.5,IP.2:10.5.0.6,IP.3:10.5.0.7,IP.4:10.5.0.8,IP.5:10.5.0.9,IP.6:10.5.0.10" -addext "extendedKeyUsage = serverAuth, clientAuth"


init: self-signed
	cp self-signed.crt node.crt
	cp self-signed.key node.key
	cp self-signed.crt node.cas
	tctl auth export --type db-client >> node.cas
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
      '    uri: "rediss://10.5.0.10:6379?mode=cluster"' \
      '    tls:' \
      '      ca_cert_file: $(CURDIR)/self-signed.crt'

.PHONY: clean
clean: down
	rm -rf node*.crt node*.cas node*.key
