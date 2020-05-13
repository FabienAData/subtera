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

data_integration:
	python input_factories/data_factory/datasets/artists.py
	python input_factories/data_factory/datasets/collaboration_songs.py
	# python input_factories/data_factory/datasets/localizations.py

net:
	python viz/network_viz/main.py
