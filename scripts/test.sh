#!/bin/bash
flake8 --exclude=.venv,snowboy,build &&
pytest --ignore=build
