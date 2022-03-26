#!/bin/bash

################################################################################
#
# Where the passed arguments are the paths to
#   1. a Metro usage CSV file
#   2. the desired output file
#
################################################################################

docker run --rm -i halpoins/wmata_pmt:latest < $1 > $2
