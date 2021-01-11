help: # @@Utils@@ Display help and exit
	@poetry run python -m makefile_help

clean: # @@Utils@@ Remove .pyc, .pyo, __pycache__, .mypy_cahce, dist
	find . \
		-type f -name '*.py[co]' -delete -o \
		-type d -name __pycache__ -delete -o \
		-type d -name '.pytest_cache' -exec rm -r "{}" + -o \
		-type d -name '.mypy_cache' -exec rm -r "{}" + -o \
		-type d -name dist -exec rm -r "{}" +

install: # @@Python@@ Install package using poetry
	poetry install

test: # @@Python@@ Run pytest in poetry environment
	poetry run pytest -vvs

build: test # @@Python@@ Build the package
	poetry build

publish: build # @@Python@@ Publish the package to PyPi
	poetry publish

publish-test: build # @@Python@@ Publish the package to test PyPi
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi