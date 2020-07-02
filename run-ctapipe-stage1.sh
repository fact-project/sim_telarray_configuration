#!/bin/bash

source environment.sh

infile=$1
outfile=$2

ctapipe-stage1-process \
    --image-extractor-type='BaselineSubtractedNeighborPeakWindowSum' \
    --input=${infile}\
    --overwrite \
    --output=${outfile}\
    --write-parameters \
    --write-images \
    --progress

rm provenance.log -f
