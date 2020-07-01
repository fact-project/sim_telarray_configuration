#!/bin/bash

source environment.sh

data_file="../data/corsika/76900/epos_urqmd_iact_lapalma_winter/gamma/00031000/corsika_gamma_run_00031718_az010-020_zd11-12.eventio.zst"
output_file="dark-simtel-output.zst"

n_events=10
n_photons=4

az=155
zd=11.5

rm ${output_directory}/${output_file} -fv


${simtel_binary} \
    -Ibuild -Iconfig \
    -C dark_events=${n_events} \
    -C laser_events=${n_events} \
    -C laser_photons=${n_photons} \
    -C telescope_zenith_angle=${zd} \
    -C telescope_azimuth=${az} \
    -c config/FACT.cfg \
    -C maximum_events=1 \
    -o ${output_directory}/${output_file} \
    -h ${output_directory}/${output_file}.hdata \
    -i ${data_file}
