TARGET=flowchart

build/${TARGET}.pdf: ${TARGET}.tex
	mkdir -p build
	lualatex --output-directory=build $^
	lualatex --output-directory=build $^

clean:
	rm -rf build
