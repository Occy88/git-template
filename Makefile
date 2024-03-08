SHELL = /bin/sh
# ENV defaults to local (so that requirements/local.txt are installed), but can be overridden
#  (e.g. ENV=production make setup).
ENV ?= local
# PYTHON specifies the python binary to use when creating virtualenv
PYTHON ?= python3.9

# Editor can be defined globally but defaults to nano
EDITOR ?= nano

# By default we open the editor after copying settings, but can be overridden
#  (e.g. EDIT_SETTINGS=no make settings).
EDIT_SETTINGS ?= yes

# Get root dir and project dir
PROJECT_ROOT ?= $(PWD)
SITE_ROOT 	 ?= $(PROJECT_ROOT)

BLACK	?= \033[0;30m
RED		?= \033[0;31m
GREEN	?= \033[0;32m
LIGHT_GREEN ?= \033[1;32m
YELLOW	?= \033[0;33m
BLUE	?= \033[0;34m
LIGHT_BLUE ?= \033[1;36m
PURPLE	?= \033[0;35m
CYAN	?= \033[0;36m
GRAY	?= \033[0;37m
COFF	?= \033[0m

INFO 	?= $(LIGHT_BLUE)
SUCCESS ?= $(LIGHT_GREEN)
WARNING ?= $(YELLOW)
ERROR 	?= $(RED)
DEBUG 	?= $(CYAN)
FORMAT 	?= $(GRAY)
BOLD ?= \033[1m

REGIONS = us-east-1
DOCKER_PREFIX = docker-compose run --rm -T app
DOCKER_PREFIX =
.PHONY: setup test hooks setup-poetry pre-commit deploy deploy-to-region build-docker deploy_ deploy-to-region_ update_requirements
setup:
	make hooks
	make build-docker
	mkdir -p packages
	touch .setup

hooks:
	cp -r hooks/* .git/hooks/

build build-docker:
build-docker:
	cp -r ~/.aws .
	mkdir -p packages
	# clear cache if necessary
	@docker volume rm sl-mr-web-data-export_precommit-cache || true
ifeq ($(shell uname -s),Darwin)
	@echo "Running on macOS, skipping USER_ID and GROUP_ID setting"
	docker-compose build
else
	@echo "Not running on macOS, setting USER_ID and GROUP_ID"
	docker-compose build --build-arg USER_ID=$(shell id -u) --build-arg GROUP_ID=$(shell id -g)
endif
update_requirements:
	@for dir in $(shell ls functions); do \
		poetry export -f requirements.txt --without-hashes --output functions/$$dir/requirements.txt --with $$dir; \
	done

setup-poetry:
	command -v poetry >/dev/null 2>&1 || { \
		curl -sSL https://install.python-poetry.org | python3 -; \
		poetry install --no-root; \
	}
	poetry env use python3.11
	poetry install

test:
	$(DOCKER_PREFIX) poetry run pytest .

pre:
pre-commit:
	poetry run pre-commit run --all-files

safety:
	poetry run safety check

build_local:
	(cd .. && dpkg-deb --build git-templates &&  sudo dpkg --install git-templates.deb)

#DEPLOY STUFF.
quality:
	make pre-commit
	make safety