CONFIG = \
		config/FACT.cfg \
		build/camera_FACT.dat \
		build/mirror_FACT.dat \
		build/pulse_shape.dat

all: test

test: build/display-dl1.png build/true_pe.png build/stage1.pdf
	pytest

build:
	mkdir -p build

build/stage1.pdf: scripts/plot_stage1.py build/events.dl1.h5
	python $<

build/pulse_shape.dat: scripts/pulse_shape.py | build
	python $<

build/events.dl1.h5: build/simtel-output.zst
	ctapipe-stage1-process --input=$< --output=$@ --overwrite --write-parameters --write-images

build/display-dl1.png: build/simtel-output.zst | build
	rm -f $@
	ctapipe-display-dl1 \
		--input $< \
		-O $@
	mv provenance.log build/

build/true_pe.png: scripts/plot_true_pe.py build/simtel-output.zst | build
	rm -f build/true_pe*
	python $<

build/simtel-output.zst: run.sh $(CONFIG) | build
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
