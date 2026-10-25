.ONESHELL:
.PHONY: all add amend beautiful black build clean commit commit-version dist echo isort jacobus py311 py312 pypi rebase reset test toml_sorted upload version
SHELL := /bin/zsh

all: beautiful commit-version

add:
	git add -A;

amend: add
	git commit --amend --no-edit;

beautiful: isort black jacobus toml_sorted

black: py311
	conda run -n py311 pip install 'black>=24.5,<26' >/dev/null;
	conda run -n py311 black --line-length=79 . ;

build: py311
	conda run -n py311 pip install 'build>=1.3,<2' >/dev/null;
	conda run -n py311 python -m build >/dev/null;

commit: add
	git commit --allow-empty $(PARAMS);

commit-version: add py311
	conda run -n py311 pip install 'toml_get>=1.0,<2' >/dev/null;
	git commit --allow-empty "$$(conda run -n py311 python -m toml_get @make/toml_get.txt)";

clean:
	rm -fr 'dist/';

dist: beautiful clean build

echo:
	echo $(PARAMS);

isort: py311
	conda run -n py311 pip install 'isort>=6.0,<7' >/dev/null;
	conda run -n py311 isort . ;

jacobus: py311
	conda run -n py311 pip install 'jacobus>=2.1,<3' >/dev/null;
	conda run -n py311 python -m jacobus @make/jacobus.txt;
	conda run -n py311 python -m jacobus @make/jacobus_in.txt;

py311:
	conda run -n base python make/env.py py311 --python=3.11;

py312:
	conda run -n base python make/env.py py312 --python=3.12;

pypi: clean build upload

rebase:
	git rebase --empty=drop --interactive $(PARAMS);

reset:
	git reset HEAD~1

test: dist
	mkdir dist/out;
	conda run -n base python make/env.py test_preparse_mypy --python=3.11 --recreate >/dev/null;
	conda run -n test_preparse_mypy pip install dist/*.tar.gz >/dev/null;
	conda run -n test_preparse_mypy pip install mypy >/dev/null;
	conda run -n test_preparse_mypy python -m mypy --exclude build --exclude dist --strict . > dist/out/mypy_dir_out.txt 2> dist/out/mypy_dir_err.txt || true;
	conda run -n test_preparse_mypy python -m mypy --strict -p preparse > dist/out/mypy_pkg_out.txt 2> dist/out/mypy_pkg_err.txt || true;
	conda run -n base python make/env.py test_preparse_tests --python=3.11 --recreate >/dev/null;
	conda run -n test_preparse_tests pip install dist/*.tar.gz >/dev/null;
	conda run -n test_preparse_tests python -c "import preparse.tests; preparse.tests.test();";


toml_sorted: py311
	conda run -n py311 pip install 'toml_sorted>=2.1,<3' >/dev/null;
	conda run -n py311 python -m toml_sorted @make/toml_sorted_data.txt;
	conda run -n py311 python -m toml_sorted @make/toml_sorted_expit.txt;
	conda run -n py311 python -m toml_sorted @make/toml_sorted_pyproject.txt;
	conda run -n py311 python -m toml_sorted @make/toml_sorted_secondary.txt;

upload: py311
	conda run -n py311 pip install 'twine>=5.2,<7' >/dev/null;
	conda run -n py311 twine upload 'dist/*';

version: all pypi
