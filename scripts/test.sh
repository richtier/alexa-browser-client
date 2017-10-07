#!/bin/bash
flake8 --exclude=.venv,venv,snowboy,build &&
pytest $1 --ignore=venv --ignore=.venv --ignore=build --cov=./ --cov-config=.coveragerc
