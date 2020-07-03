#!/bin/bash

source environment.sh

infile=$1
outfile=$2
logfile=${outfile}.log
histfile=${outfile}.hdata

for k in $(${SIM_TELARRAY_PATH}/bin/extract_corsika_tel --header-only --only-telescopes 1 "${infile}"); do
    echo "export $k";
    export $k;
done

${simtel_binary} \
    -Ibuild -Iconfig \
    -C telescope_theta="${CORSIKA_THETA:-0.0}" \
    -C telescope_phi="${CORSIKA_PHI:-0}" \
    -c config/FACT.cfg \
    -C show=all \
    -h ${histfile} \
    -o ${outfile} \
    -i ${infile} \
    | gzip > ${logfile}
