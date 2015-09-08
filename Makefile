
make:
	python make.py make

clean:
	python make.py clean

install: make
	python make.py install

.PHONY: make