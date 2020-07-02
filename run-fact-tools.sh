#!/bin/bash

source environment.sh

infile=$1
outfile=$2

java -jar ${fact_tools_jar} \
    scripts/save_dl1_mc.xml \
    --infile=file:${infile} \
    --drsfile=file:build/testMcDrsFile.drs.fits.gz \
    --pixelDelayFile=file:build/delays_zero.csv \
    --outfile=file:${outfile}
