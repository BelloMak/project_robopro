test:
	pytest --cov=roboter/

lint:
	ruff check --fix

format:
	ruff format

update_req:
	uv export --no-hashes --format requirements-txt > requirements.txt

.PHONY: test 
