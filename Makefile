all: flake8 pyright cov

flake8:
	pipenv run flake8

pyright:
	pipenv run yarn run pyright

cov:
	pipenv run pytest --cov tmux_super_fingers --cov-branch

hcov:
	pipenv run pytest --cov tmux_super_fingers --cov-branch --cov-report=html

test:
	pipenv run pytest
