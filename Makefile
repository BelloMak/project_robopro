test:
	pytest --cov=roboter/

lint:
	ruff check --fix

format:
	ruff format

requirements:
	uv export --no-hashes --format requirements-txt > requirements.txt

server:
	gcc ./assignment/server.c -o server.prog

run:
	uv run ./start_robot_terminal.py

.PHONY: test 
