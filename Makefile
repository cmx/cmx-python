# shell option to use extended glob from https://stackoverflow.com/a/6922447/1560241
SHELL:=/bin/bash -O extglob

VERSION := $(shell cat VERSION)
PACKAGE_NAME := cmx

# notes on python packaging: http://python-packaging.readthedocs.io/en/latest/minimal.html
.PHONY: default wheel dev convert-rst resize update-doc prepare release publish publish-no-test test preview docs clean update-plugin

default: publish release

wheel:
	rm -rf dist build
	python -m build

dev: wheel
	pip install --ignore-installed dist/$(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl

convert-rst:
	pandoc -s README.md -o README --to=rst
	sed -i '' 's/code:: /code-block:: /g' README
	sed -i '' 's/\.\. code-block:: log/.. code-block:: text/g' README
	sed -i '' 's/\.\//https\:\/\/github\.com\/cmx\/cmx-python\/blob\/main\//g' README
	perl -p -i -e 's/\.(jpg|png|gif)/.$$1?raw=true/' README

resize: # from https://stackoverflow.com/a/28221795/1560241
	@echo ./figures/!(*resized).jpg
	convert ./figures/!(*resized).jpg -resize 888x1000 -set filename:f '%t' ./figures/'%[filename:f]_resized.jpg'

update-doc: convert-rst
	python setup.py sdist upload

preview:
	@echo "Starting documentation preview at http://localhost:8888"
	sphinx-autobuild docs docs/_build/html --port 8888 --open-browser

docs:
	@echo "Building documentation..."
	cd docs && make clean && make html
	@echo "Documentation built! Open docs/_build/html/index.html"
	python -m http.server 8888 --directory docs/_build/html

update-plugin:
	@echo "Updating Claude plugin version to $(VERSION)..."
	python3 .claude-plugin/generate_plugin_json.py

prepare: update-plugin
	# Remove existing tags
	git tag -d $(VERSION) || true
	git push origin :refs/tags/$(VERSION) || true

# Do NOT create a git tag named `latest`: Read the Docs treats a branch or tag
# named `latest` as the "latest" docs version, shadowing its default behavior
# of building `latest` from the default branch (main) on every push.
release: prepare
	git add -A
	git commit -m "Release version $(VERSION)" || true
	git push
	git tag v$(VERSION) -m "$(msg)"
	git push origin --tags

publish-no-test: convert-rst wheel
	twine upload dist/*

publish: convert-rst test wheel
	twine upload dist/*

test:
	@echo "Running tests..."
	python -m pytest tests --capture=no

clean:
	rm -rf build dist *.egg-info
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

