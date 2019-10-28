build:
	rm -rf build
	rm -rf dist
	python setup.py bdist_wheel


publish_test:
	make build
	twine upload -r pypitest dist/*


publish:
	make build
	twine upload dist/*


test_requirements:
	pip install -e .[test]


demo:
	python3 ./demo/manage.py runserver


.PHONY: demo publish_test publish build
