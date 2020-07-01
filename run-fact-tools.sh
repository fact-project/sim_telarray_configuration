#!/bin/bash

source environment.sh

infile=$1
outfile=$2

java -jar ${fact_tools_jar} \
    ${fact_tools_git_dir}/examples/save_dl1.xml \
    --infile=file:${infile} \
    --drsfile=file:${fact_tools_git_dir}/src/main/resources/testMcDrsFile.drs.fits.gz \
    --pixelDelayFile=file:${fact_tools_git_dir}/src/main/resources/default/delays_zero.csv \
    --outfile=file:${outfile}
