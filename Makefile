setup:
	python3 -m venv envasl
	pip3 install -r requirements.txt

dev:
	python -m flask --debug run --host=0.0.0.0 --port=5000
