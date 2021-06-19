test: clean
	pytest

run:
	python src/cafe/simulateCoOp.py --farm data/fakeData.csv --trees data/trees.yml --years 30 --output testNewFarm.png

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

