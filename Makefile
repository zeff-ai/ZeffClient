.POSIX:
.PHONY: publish validate build test lint help

PIP = python -m pip
PIPFLAGS = --quiet


install:			## Install dependencies in virtualenv
	python setup.py install


publish:			## Publish the library to the central PyPi repository
	echo python setup.py sdist upload


validate: build lint test	## Validate project for CI, CD, and publish


docs:				## Create documentation
	python -c 'import zeff; print(zeff.__doc__)' | \
		sed '1,3d' | \
		rst2man.py > spam.man


clean:				## Clean generated files
	@rm -rf build
	@rm -rf dist
	@rm -rf sdist
	@rm -rf var
	@rm -rf tmp
	@rm -rf .eggs
	@rm -rf *.egg-info
	@rm -rf pip-wheel-metadata
	@find zeff -name '__pycache__' -exec rm -rf {} \; -prune


clean_cache:		## Clean caches
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf coverage_html_report
	@rm -rf .mypy_cache
	@rm -rf .hypothesis


build:				## Build into ``./build`` directory
	python setup.py build


test: build dependencies_test	## Run test suite
	python -m pytest --cov=zeff && \
		coverage html


lint:				## Check source for conformance
	@echo Checking source conformance
	pylint -f parseable -r n zeff && \
		pycodestyle zeff && \
		pydocstyle zeff 

#mypy zeff 



###
### Dependencies

.PHONY: dependencies dependencies_docs dependencies_test

dependencies: dependencies_docs dependencies_test  ## Install dependencies in the current virtualenv

dependencies_docs:
	@echo Install documentation dependencies
	${PIP} ${PIPFLAGS} install --upgrade ".[docs]"

dependencies_test:
	@echo Install test dependencies
	${PIP} ${PIPFLAGS} install --upgrade ".[tests]"


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

