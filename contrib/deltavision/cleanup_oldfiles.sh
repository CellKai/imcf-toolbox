#!/bin/bash

# exit immediately in case of an error:
set -e

BASEDIR="/data1"
 
AGE_Y=0  # Years
AGE_M=6  # Months (averaged to 30 days)
AGE_D=0  # Days

# create a string with dashes that has the same length as "$0":
FILL_DASH=${0//?/-}
FILL_EQAL=${0//?/=}

echo -e "===== $0 =====\n"
hostname
echo -e "\n------$FILL_DASH------\n"
df -h
echo -e "------$FILL_DASH------\n"

cd "$BASEDIR"
pwd
 
# calculate mtime by values from above
MTIME=$(($AGE_Y * 365 + $AGE_M * 30 + $AGE_D))

echo "Cleaning up files older than $MTIME days, which is:"
echo "    * $AGE_Y years"
echo "    * $AGE_M months"
echo "    * $AGE_D days"
echo
 
find -name '*.tif' -mtime +$MTIME -type f -print0 \
    -or -name '*.dv' -mtime +$MTIME -type f -print0 \
    -or -name '*.dv.log' -mtime +$MTIME -type f -print0 \
    -or -name '*_log.txt' -mtime +$MTIME -type f -print0 \
    -or -name '*.jpg' -mtime +$MTIME -type f -print0 | xargs -0 --no-run-if-empty rm -v

echo -e "------$FILL_DASH------\n"
df -h
echo -e "======$FILL_EQAL======\n"
