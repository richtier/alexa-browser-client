#!/bin/bash
flake8 --exclude=.venv,venv,snowboy,build &&
pytest --ignore=venv --ignore=.venv --ignore=build --cov=./ --cov-config=.coveragerc
