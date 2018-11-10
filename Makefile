lint:
	flake8 --exclude=.venv,venv,snowboy,build


test:
	pytest $1 \
		--ignore=venv \
		--ignore=.venv \
		--ignore=build \
		--cov=./ \
		--cov-config=.coveragerc \
		--capture=no \
		--last-failed \
		--verbose


publish_test:
	rm -rf build &&
	rm -rf dist &&
	python setup.py bdist_wheel &&
	twine upload -r pypitest dist/*


publish:
	twine upload dist/*


demo:
	python3 ./demo/manage.py runserver


.PHONY: lint pytest demo publish_test publish
