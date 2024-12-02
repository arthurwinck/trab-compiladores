# Python 3.12.4

env: requirements.txt
	python -m venv env
	./env/bin/pip install -r requirements.txt

run: env
	./env/bin/python main.py