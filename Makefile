run:
	python ./main.py

freeze:
	pip freeze > pip_requirements

install_packages:
	pip install -r pip_requirements