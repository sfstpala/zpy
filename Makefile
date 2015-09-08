# Copyright (C) 2015  Stefano Palazzo <stefano.palazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
