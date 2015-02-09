!/bin/bash
echo Get certificate
getCert
echo Making dirs
mkdir -p ${TMPDIR}/{vos,vos_cache,proc,vos_link}
echo Mount VOS in readonly mode
mountvofs --vospace vos:MWSynthesis/SextansA_test/ --mountpoint ${TMPDIR}/vos --ca$
echo Sourcing
source /home/cloud-user/.bashrc
cd ${TMPDIR}/proc
vcp vos:MWSynthesis/casanfar_image3.py .
echo Run casapy and casanfar_image3.py
casapy --nogui --nologger -c casanfar_image3.py
echo Unmount VOS
fusermount -zu ${TMPDIR}/vos
echo Mount VOS
mountvofs --vospace vos:MWSynthesis/SextansA_test/ --mountpoint ${TMPDIR}/vos --ca$
echo Copy files to VOS
cp -rf ${TMPDIR}/proc/* ${TMPDIR}/vos/
echo Unmount VOS
fusermount -zu ${TMPDIR}/vos
