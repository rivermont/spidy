all_targets: lint test clean-pyc clean-build clean-crawler

lint:
	flake8 *.py

test:
	python3 ./spidy/tests.py
	rm -rf ./logs ./saved

clean-pyc:
	rm -rf ./spidy/__pycache__
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

clean-build:
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info

clean-crawler:
	-rm -rf ./spidy/logs
	-rm -rf ./spidy/saved
	find . -name "*.txt" -not -name "requirements.txt" -delete
	find . -name "None" -delete

help:
	@echo "    lint"
	@echo "        Check PEP8 compliance with flake8."
	@echo "    test"
	@echo "        Run all tests in spidy/tests.py."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    clean-crawler"
	@echo "        Remove crawler artifacts."
