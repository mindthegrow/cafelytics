test:
	pytest

run:
	python3 src/cafe/simulateCoOp.py --farm data/fakeData.csv --trees data/trees.yml --years 75 --output testNewFarm.png

data:
	python3 src/cafe/fakeData.py --farms 100 --year 2020 --output data/fakeData.csv

build: clean
	python setup.py sdist bdist_wheel

lint:
	flake8 src/
	flake8 tests/

black:
	black .

cov: test
	coverage html
	open htmlcov/index.html

clean:
	rm -rf tests/.ipynb_checkpoints
	rm -f  .coverage
	rm -rf .pytest_cache/
	rm -rf .eggs/
	rm -rf .ipynb_checkpoints
	rm -rf src/cafe/.ipynb_checkpoints
	rm -rf binder/.ipynb_checkpoints
	rm -rf __pycache__/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf src/cafelytics.egg-info/


version:
	git describe --always --dirty --tags --long --match "*[0-9]*"

publish:
	rm -rf dist/*
	python -m pip install -U pip wheel setuptools setuptools_scm twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
