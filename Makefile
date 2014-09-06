test:
	python -m unittest discover tests/

clean:
	rm -f `find . -name '*.pyc'`
