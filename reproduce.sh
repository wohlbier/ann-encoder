#!/bin/bash

# get data from the address provided in the email.
# set your CACHE_PATH
CACHE_PATH=/local/devel/SDH/DATA/SDH

# these are variables for the Intel OpenMP runtime. If you roll back to
# Python 3.6 you might need to change to the libgomp variables to get the
# desired affinity.
OMP_DISPLAY_ENV=true OMP_NUM_THREADS=24 KMP_AFFINITY=granularity=fine,compact,1,0 KMP_HW_SUBSET=1s,24c,2t map --profile python train.py --cache-path ${CACHE_PATH}/netflix --emb-dim 256 --batch-size 16
