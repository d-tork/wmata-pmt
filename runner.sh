#!/bin/bash

################################################################################
#
# Where the passed argument is the path to a Metro usage CSV file
#
################################################################################

docker run --rm -i -v $(pwd):/data wmata_pmt:latest < $1
