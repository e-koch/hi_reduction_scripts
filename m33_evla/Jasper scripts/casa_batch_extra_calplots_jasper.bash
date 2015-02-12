#!/bin/bash

# Load in casa pointer
echo 'Sourcing'
source /home/ekoch/.bashrc

# Make sure we're on the right branch
cd /home/ekoch/code_repos/hi_reduction_scripts
git checkout EVLA_pipeline

# Specify MSfile
ms_folder='14B-088_20141021_1413960928386/'
ms_file='14B-088.sb29701604.eb29882607.56952.08797296297.ms'


cd /home/ekoch/m33/${ms_folder}'products/'

# Copy the necessary code
mkdir EVLA_pipeline1.3.0/
cp /home/ekoch/code_repos/hi_reduction_scripts/m33_evla/EVLA_pipeline1.3.0/* EVLA_pipeline1.3.0/
cp /home/ekoch/code_repos/hi_reduction_scripts/m33_evla/spw_plots.py .

# Run the code
echo "Run casapy and spw_plots.py"
/home/ekoch/casapy-42.2.30986-1-64b/casapy --nogui --nologger -c spw_plots.py ms_file

mkdir spw_plots

mv *.png spw_plots

# Clean-up
rm -rf EVLA_pipeline1.3.0
rm spw_plots.py
