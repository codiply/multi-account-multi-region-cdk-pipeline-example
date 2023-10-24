.PHONY: help compile-requirements pre-commit

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

requirements/requirements.txt: requirements/requirements.in
	pip-compile $<
	touch $@

requirements/requirements-dev.txt: requirements/requirements-dev.in requirements/requirements.in
	pip-compile $<
	touch $@

compile-requirements: requirements/requirements.txt requirements/requirements-dev.txt # Compile all requirements files

pre-commit: # Run all pre-commit hooks on all files
	pre-commit run --all-files
