python=python3

all: zpy.egg-info
zpy.egg-info: bin/pip setup.py
	$< install --editable . && touch $@
bin/pip: bin/python
	curl https://bootstrap.pypa.io/get-pip.py | bin/python
bin/python:
	$(python) -m venv . --without-pip

test: all
	$(MAKE) coverage
	$(MAKE) flake8
	$(MAKE) check
coverage: all bin/coverage
	bin/coverage run setup.py test
	bin/coverage html
	bin/coverage report --fail-under=100
bin/coverage: bin/pip
	bin/pip install coverage
flake8: bin/flake8
	bin/flake8 --max-complexity=10 setup.py zpy
bin/flake8: bin/pip
	bin/pip install flake8
check: bin/check-manifest
	bin/check-manifest
	bin/python setup.py check -ms
bin/check-manifest: bin/pip
	bin/pip install check-manifest

wheels: all test
	rm -rf wheelhouse; bin/pip wheel .

clean:
	rm -rf dist build *.egg-info $(shell find zpy -name __pycache__)
	rm -rf bin lib lib64 include pip-selfcheck.json pyvenv.cfg
	rm -rf htmlcov .coverage .tox wheelhouse
