test: clean
	pytest

clean:
	rm -rf tests/.ipynb_checkpoints

run:
	python src/cafe/simulateCoOp.py --farm data/fakeData.csv --trees data/trees.yml --years 30 --output testNewFarm.png
