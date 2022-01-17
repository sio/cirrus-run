ARGS?=--help


ifdef DEBUG
TWINE_ARGS+=--repository-url "https://test.pypi.org/legacy/"
endif


.PHONY: run
run: | venv
	$(VENV)/cirrus-run $(ARGS)


.PHONY: test
REQUIREMENTS_TXT+=tests/requirements.txt
test: | venv
	$(VENV)/pytest $(PYTEST_ARGS)


.PHONY: test-job
test-job: | venv
	$(VENV)/cirrus-run tests/sample_build_config.yml -vvvv --show-build-log=always


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2020.02.26/Makefile.venv"
	echo "e0aeebe87c811fd9dfd892d4debb813262646e3e82691e8c4c214197c4ab6fac *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv


.PHONY: package
package: | venv
	-rm -rv dist
	$(VENV)/python setup.py sdist


.PHONY: upload
upload: package $(VENV)/twine
	$(VENV)/twine upload $(TWINE_ARGS) dist/*
