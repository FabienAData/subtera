NOTEBOOKSDIR = notebooks

.PHONY: notebooks

install:
	pip install -r requirements.txt

update:
	pip freeze > requirements.txt

check:
	flake8 modules/ data_factory/ tests/
	mypy .

test:
	pytest tests/

map:
	python data_factory/datasets/scientists.py
	python data_factory/datasets/artists.py
	python data_factory/datasets/localizations.py
	python map_viz/main.py
	google-chrome ~/Bureau/map.html
