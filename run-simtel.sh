#!/bin/bash

simtel_bin="../simtel/sim_telarray/sim_telarray"

AZ=155
ZD=11.5

infile=$1
outfile=$2

${simtel_bin} \
    -Ibuild -Iconfig \
    -C telescope_theta=${ZD} \
    -C telescope_phi=${AZ} \
    -c config/FACT.cfg \
    -o ${outfile} \
    -i ${infile}
