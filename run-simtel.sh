#!/bin/bash

source environment.sh

infile=$1
outfile=$2
logfile=${outfile}.log
histfile=${outfile}.hdata

for k in $(${SIM_TELARRAY_PATH}/bin/extract_corsika_tel --header-only --only-telescopes 1 "${infile}"); do
    export $k;
done

offset=0.6

${simtel_binary} \
    -Ibuild -Iconfig \
    -C random_state=auto \
    -C telescope_theta=$(echo "${CORSIKA_THETA:-0.0} + ${offset}" | bc -l) \
    -C telescope_phi="${CORSIKA_PHI:-0}" \
    -c config/FACT.cfg \
    -C show=all \
    -h ${histfile} \
    -o ${outfile} \
    -i ${infile} \
    2>&1 | zstd > ${logfile}
