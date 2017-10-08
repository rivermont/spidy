all_targets: lint test clean-pyc clean-build clean-spidy

lint:
	flake8 --ignore=E501 *.py

test:
	python3 ./spidy/tests.py

clean-pyc:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

clean-build:
	-rm -rf build
	-rm -rf dist

clean-spidy:
	-rm -rf ./spidy/logs
	-rm -rf ./spidy/saved

help:
	@echo "    lint"
	@echo "        Check PEP8 compliance with flake8."
	@echo "    test"
	@echo "        Run all tests in spidy/tests.py."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    clean-spidy"
	@echo "        Remove crawler artifacts."
