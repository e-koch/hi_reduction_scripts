#!/bin/bash
echo Get certificate
getCert
echo Sourcing
source /home/dcolombo/.bashrc
echo Copying files
vcp vos:dcolombo/cloudstering2/MILKY_WAY/cygx.fits ${TMPDIR}/
vcp vos:dcolombo/cloudstering2/MILKY_WAY/cygx_dilmasked.fits ${TMPDIR}/
echo Copying script
vcp vos:dcolombo/dendro2cata_9.py /home/dcolombo/dendro_scripts/
cd ${TMPDIR}/
chmod 755 /home/dcolombo/dendro_scripts/dendro2cata_9.py
/home/dcolombo/dendro_scripts/dendro2cata_9.py
