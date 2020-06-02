CONFIG = \
		config/FACT.cfg \
		build/camera_FACT.dat \
		build/mirror_FACT.dat

all: test

test: build/display-dl1.png build/true_pe.png
	pytest

build:
	mkdir -p build

build/display-dl1.png: build/simtel-output.zst | build
	rm -f $@
	ctapipe-display-dl1 \
		--input $< \
		-O $@
	mv provenance.log build/

build/true_pe.png: scripts/plot_true_pe.py build/simtel-output.zst | build
	rm -f build/true_pe*
	python $<

build/simtel-output.zst: $(CONFIG) | build
	rm -f $@
	./run.sh
	mv telarray_rand.conf.used build/

build/mirror_FACT.dat: scripts/convert_mirror.py config/reflector.txt | build
	python $<

build/camera_FACT.dat: scripts/camera.py | build
	python $<

.PHONY: all clean test

clean:
	rm -rf build
