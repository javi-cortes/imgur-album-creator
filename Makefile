help:
	@echo "help                               -- prints this help"
	@echo "build                              -- builds Docker containers"
	@echo "run                                -- run spider"
	@echo "list-spiders                       -- list all spiders"

# @ is to hide the echo of the command
# dkc = docker-compose -f docker-compose.dev.yml -f docker-compose.override.yml $arguments

GREEN="\\e[32m"
BLUE="\\e[94m"
REGULAR="\\e[39m"
RED="\\e[91m"

run:
	docker run -it imgur-crawler

auth:
	docker run -it imgur-crawler python3 imgur_crawler/imgur_handler.py

list-spiders:
	docker run imgur-crawler scrapy list

build:
	docker build . -t imgur-crawler

.PHONY: help build run list-spiders
