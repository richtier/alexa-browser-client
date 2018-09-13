#!/bin/bash
rm -rf build
rm -rf dist
python setup.py bdist_wheel
twine upload -r pypitest dist/*
