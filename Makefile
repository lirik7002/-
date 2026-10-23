run:
	python -m src.main --vfs vfs_samples/nested.xml --script starter_script.txt

test:
	pytest -q

lint:
	ruff check src/ tests/

.PHONY: run test lint
