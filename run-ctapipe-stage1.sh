#!/bin/bash

version=$(ctapipe-stage1-process --version)
outdir="ctapipe-stage1/${version}/"
mkdir -p ${outdir}

infile=$1
outfile=$2

ctapipe-stage1-process \
    --image-extractor-type='BaselineSubtractedNeighborPeakWindowSum' \
    --input=${infile}\
    --overwrite \
    --output=${outfile}\
    --write-parameters \
    --progress

rm provenance.log -f
