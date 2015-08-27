TARGET=flowchart

build/${TARGET}.pdf: ${TARGET}.tex
	mkdir -p build
	latexmk -lualatex -output-directory=build ${TARGET}

clean:
	rm -rf build

open: build/${TARGET}.pdf
	open $^
