#!/bin/bash

SIMTEL=../simtel/sim_telarray
DATA=../data
DATA_FILE=corsika_*_run_0003****_az01*-0**_zd**-**.eventio.zst
OUTPUT_PATH=build/simtel

AZ=155
ZD=11.5

rm ${OUTPUT_PATH} -f

${SIMTEL}/sim_telarray \
    -Ibuild -Iconfig \
    -C plot_file=build/simtel_plot \
    -C telescope_zenith_angle=${ZD} \
    -C telescope_azimuth=${AZ} \
    -c config/FACT.cfg \
    -o ${OUTPUT_PATH}-output.zst \
    -p ${OUTPUT_PATH}-plots \
    -h ${OUTPUT_PATH}-hist \
    -i ${DATA}/${DATA_FILE} \

echo "processed ${DATA_FILE}"
