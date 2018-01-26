all: dependencies

dependencies:
	pip install -q -U -r requirements.txt

dev-dependencies:
	pip install -q -U -r requirements.txt -r requirements-dev.txt

lint: lint-codestyle lint-docstring

lint-codestyle: dev-dependencies
	pycodestyle --show-pep8 --show-source ./

lint-docstring: dev-dependencies
	pydocstyle --explain --source ./

test: clean lint unittest

unittest: dev-dependencies
	python -m unittest discover

coverage: clean-coverage dev-dependencies lint
	coverage run --source action_plugins test
	coverage html
	coverage report

docs: clean-docs dev-dependencies
	pydoc -w action_plugins

changelog:
	$(eval TAG2 := $(shell git describe --tags --abbrev=0 2>/dev/null || echo "HEAD"))
	$(eval TAG1 := $(shell (git describe --tags --abbrev=0 $(TAG2)~1 2>/dev/null | xargs -I % echo %..) || echo ""))

	$(info Changelog for $(TAG1)$(TAG2):)
	$(info )
	@git log $(TAG1)$(TAG2) --no-merges --reverse --pretty=format:'- [view](https://github.com/andrewvaughan/ansible-role-prompt/commit/%H) &bull; %s'

clean: clean-ansible clean-python clean-coverage clean-docs

clean-ansible:
	find . -name '*.retry' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

clean-python:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-coverage:
	rm -rf .coverage htmlcov

clean-docs:
	rm -rf *.html

.PHONY : all dependencies dev-dependencies lint lint-codestyle lint-docstring test unittest coverage docs changelog clean clean-ansible clean-python clean-coverage clean-docs
