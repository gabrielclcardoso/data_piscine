all:
	docker-compose up -d

down:
	docker-compose down

.PHONY:
	all down
