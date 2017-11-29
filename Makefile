dependencies:
	pip install -q -U -r requirements.txt

dev-dependencies: dependencies
	pip install -q -U -r requirements-dev.txt

lint: dev-dependencies lint-docstring
	pycodestyle --show-pep8 --show-source ./

lint-docstring: dev-dependencies
	pydocstyle --explain --source ./

test: clean dev-dependencies lint
	python -m unittest discover

coverage: clean dev-dependencies lint
	coverage run --source action_plugins test
	coverage html
	coverage report

docs: clean dev-dependencies
	pydoc -w action_plugins

changelog:
	$(eval TAG2 := $(shell git describe --tags --abbrev=0 2>/dev/null || echo "HEAD"))
	$(eval TAG1 := $(shell (git describe --tags --abbrev=0 $(TAG2)~1 2>/dev/null | xargs -I % echo %..) || echo ""))

	$(info Changelog for $(TAG1)$(TAG2):)
	$(info )
	@git log $(TAG1)$(TAG2) --no-merges --reverse --pretty=format:'- [view](https://github.com/andrewvaughan/ansible-prompt/commit/%H) &bull; %s'

clean:
	rm -rf .coverage htmlcov
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	find . -name '*.retry' -exec rm -f {} +

.PHONY : dependencies dev-dependencies lint lint-docstring test coverage docs changelog clean
