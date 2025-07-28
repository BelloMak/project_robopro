test:
	pytest --cov=roboter/

lint:
	ruff check --fix

format:
	ruff format

update_req:
	uv export --no-hashes --format requirements-txt > requirements.txt

server:
	gcc ./assignment/server.c -o server.prog

.PHONY: test 
