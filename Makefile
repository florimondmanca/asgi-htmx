venv = venv
bin = ${venv}/bin/
pysources = src tests/ examples/

build:
	${bin}python -m build

check:
	${bin}black --check --diff ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}

install:
	python3 -m venv ${venv}
	${bin}pip install -U pip wheel
	${bin}pip install -U build
	${bin}pip install -r requirements.txt

format:
	${bin}autoflake --in-place --recursive ${pysources}
	${bin}isort ${pysources}
	${bin}black ${pysources}

publish:
	${bin}twine upload dist/*

test:
	${bin}pytest
