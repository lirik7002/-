.PHONY: install test run-demo lint

install:
	pip install -r requirements-dev.txt

test:
	pytest -q

run-demo:
	python -m src.main \
		--package=A \
		--repo=tests/fixtures/test_repo.txt \
		--mode=test \
		--output=out/demo.png \
		--exclude=

lint:
	python -m compileall -q src tests
