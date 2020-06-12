CONFIG = \
		config/FACT.cfg \
		build/camera_FACT.dat \
		build/mirror_FACT.dat \
		build/pulse_shape.dat

all: test build/hillas.pdf build/laser_waveforms.png build/waveforms.png build/display-dl1.pdf build/intensity.png

test: build/pytest.out

build/pytest.out: | build
	pytest -q | tee $@

build:
	mkdir -p build

build/pulse_shape.dat: scripts/pulse_shape.py | build
	python $<

build/hillas.pdf: scripts/hist_hillas.py build/events.dl1.h5
	python $<

build/events.dl1.h5: build/simtel-output.zst
	ctapipe-stage1-process \
		--input=$< \
		--output=$@ \
		--overwrite \
		--write-parameters \
		--write-images \
		--progress
	mv provenance.log build/

build/display-dl1.pdf: build/simtel-output.zst | build
	rm -f $@
	ctapipe-display-dl1 \
		--input $< \
		--ImagePlotter.display=False \
		--max_events=10 \
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

build/waveforms.png: scripts/waveforms.py build/simtel-output.zst | build
	python $<

build/laser_waveforms.png: scripts/laser_waveforms.py build/simtel-output.zst | build
	python $<

build/pulse_shape.png: scripts/plot_pulse.py build/pulse_shape.dat
	python $<

build/energy.png: scripts/plot_energy.py build/simtel-output.zst
	python $<

.PHONY: all clean test

clean:
	rm -rf build
