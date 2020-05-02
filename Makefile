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
