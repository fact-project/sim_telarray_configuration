#!/bin/bash

fact_tools_git_dir="${HOME}/Uni/fact-tools/"
fact_tools_bin="${HOME}/Downloads/fact-tools-v1.1.3.jar"
version=$(java -jar ${fact_tools_bin} --version | awk '/project version/ {print $3}')

outdir="fact-tools/${version}/"
mkdir -p ${outdir}

infile=$1
outfile=$2

java -jar ${fact_tools_bin} \
    ${fact_tools_git_dir}/examples/save_dl1.xml \
    --infile=file:${infile} \
    --drsfile=file:${fact_tools_git_dir}/src/main/resources/testMcDrsFile.drs.fits.gz \
    --pixelDelayFile=file:${fact_tools_git_dir}/src/main/resources/default/delays_zero.csv \
    --outfile=file:${outfile}
