#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
# :Author: Lance Finn Helsten <lanhel@zeff.ai>
# :Copyright: Copyright © 2019, Ziff, Inc. — All Rights Reserved
# :License:
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
.POSIX:

SETUP         = python -m setup
SETUPFLAGS    =
PIP           = python -m pip
PIPFLAGS      = --quiet

.PHONY: install
install:			## Install system
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	${SETUP} ${SETUPFLAGS} install


# Publish requires a username & password for twine to upload to PyPI
# ``export TWINE_USERNAME=<username>``
# ``export TWINE_PASSWORD=<password>``
#
# For automated upload with API token the following is required:
# ``export TWINE_USERNAME=__token__``
# ``export TWINE_PASSWORD=pypi-<token_value>``
.PHONY: publish
publish: clean		## Publish the library to the central PyPi repository
	${PIP} ${PIPFLAGS} install --upgrade pip setuptools wheel twine
	${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"
	${SETUP} ${SETUPFLAGS} sdist bdist_wheel
	python -m twine check dist/*
	python -m twine upload --verbose dist/*
	@$(MAKE) -C docs publish


.PHONY: docs
docs:				## Create documentation
	@echo Update documentation tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"
	@echo Create documentation
	@$(MAKE) -C docs docs


.PHONY: examples
examples:			## Setup environement for doing examples
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[examples]"
	${SETUP} ${SETUPFLAGS} build install


.PHONY: validate
validate: lint test	## Validate project for CI, CD, and publish


clean:				## Clean generated files
	@$(MAKE) -C docs clean
	@rm -rf build
	@rm -rf dist
	@rm -rf sdist
	@rm -rf var
	@rm -rf tmp
	@rm -rf .eggs
	@rm -rf *.egg-info
	@rm -rf pip-wheel-metadata
	@find src -name '__pycache__' -exec rm -rf {} \; -prune
	@find tests -name '__pycache__' -exec rm -rf {} \; -prune


clean_cache:		## Clean caches
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf coverage_html_report
	@rm -rf .mypy_cache
	@rm -rf .hypothesis


.PHONY: build
build:				## Build into ``./build`` directory
	@echo Updating build tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	${SETUP} ${SETUPFLAGS} build


.PHONY: test
test:				## Run test suite
test: build
	@echo Updating test tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[tests]"
	coverage run && coverage report && coverage html


.PHONY: lint
lint:				## Check source for conformance
	@echo Checking source conformance
	@echo Updating lint tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[lint]"
	black --check setup.py src tests
	pylint -f parseable -r n src
	pycodestyle src
	pydocstyle src
	mypy src


format:				## Format source code to standard
	@echo Formatting source
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[dev]"
	find src -name '*.py' -exec black -q {} \;
	find tests -name '*.py' -exec black -q {} \;


updatedev:			## Update / init all packages for development environment
	${PIP} ${PIPFLAGS} install --upgrade pip
	${PIP} ${PIPFLAGS} install --upgrade -e .
	${PIP} ${PIPFLAGS} install --upgrade -e ".[dev]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[tests]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[lint]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

