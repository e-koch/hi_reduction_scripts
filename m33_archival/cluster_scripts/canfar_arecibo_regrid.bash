#!/bin/bash

# Grab the certificate
echo Get certificate
getCert

# Make some temporary directories
echo "Making dirs"
mkdir -p ${TMPDIR}/{vos,vos_cache,proc,vos_link}

# Mount VOSpace
echo "Mount VOS in readonly mode"
mountvofs --vospace vos:MWSynthesis/ --mountpoint ${TMPDIR}/vos --ca$

# Copy the necessary code
cd ${TMPDIR}/proc

git clone https://github.com/e-koch/hi_reduction_scripts.git
cd hi_reduction_scripts
git checkout EVLA_pipeline
cd ..

# Specify file locations
arecibo_mask = ${TMPDIR}/vos/Arecibo/M33only_jy_5sigmask.fits
vla_cube = ${TMPDIR}/vos/VLA/archival/M33_206_b_c.dirty.altered.fits

# Create CLEAN mask from Arecibo data
echo "Starting at: `date`"
python hi_reduction_scripts/m33_archival/arecibo_mask/match_regrid_cubes.py ${arecibo_mask} ${vla_cube} M33_arecibo_clean_mask.fits
echo "Exited with code $? at: `date`"

# Remove code repo
rm -rf hi_reduction_scripts

# Unmount VOSpace and copy output back over.
echo 'Unmount VOS'
fusermount -zu ${TMPDIR}/vos
echo 'Mount VOS'
mountvofs --vospace vos:MWSynthesis/VLA/archival --mountpoint ${TMPDIR}/vos --ca$
echo 'Copy files to VOS'
cp -rf ${TMPDIR}/proc/* ${TMPDIR}/vos/
echo 'Unmount VOS'
fusermount -zu ${TMPDIR}/vos