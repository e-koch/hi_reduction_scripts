
'''
M33 Archival VLA Data
Make the cube
'''

import os

from tasks import *
from taskinit import *
import casac

do_cvel = False
do_cont_image = False
do_plotcontsub = False
do_contsub = False
do_plotsub = False
do_image = True
do_clean_1chan = False
do_clean = False
do_export = False


vis = "M33_bconfig_all.split"
out_root = "M33_bconfig_all"

if do_cvel:

    os.system('rm -rf '+out_root+'.cvel')
    cvel(vis=vis, outputvis=out_root+'.cvel', mode='velocity',
         nchan=-1, start=0, width=1, restfreq='1420.40575177MHz',
         outfram='LSRK')

if do_cont_image:
  # Image the continuum, just to take a look.

    clean(vis=vis, imagename=out_root+'.continuum_mfs',
          restfreq='1420.40575177MHz', multiscale=[0, 3, 9, 27],
          mode='mfs', width=1, nchan=30, start=195, cell='1.5arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=0,
          pbcor=False, interpolation='linear', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79')

if do_plotcontsub:

    print "Plotting amp. vs. chan"

    plotms(vis=vis, field="M33*", xaxis='chan', yaxis='amp', avgtime='1e8s',
           avgscan=True, avgbaseline=False)
    wait = raw_input("Continue?")

if do_contsub:

    print "Subtracting continuum."

    os.system('rm -rf '+out_root+'.contsub')

    uvcontsub(vis=vis, field="M33*", combine='spw', solint='int', fitorder=0,
              fitspw='0~1:20~30,195~225')

if do_plotsub:

    print "Plotting amp. vs. chan"

    vis = vis + '.contsub'

    plotms(vis=vis, field="M33*", xaxis='chan', yaxis='amp', avgtime='1e8s',
           avgscan=True, avgbaseline=False)
    wait = raw_input("Continue?")


if do_image:

    vis = vis + '.contsub'

    # First creates a dirty cube to examine

    print "Making dirty cube."

    os.system('rm -rf '+out_root+'.dirty*')

    mask = None

    clean(vis=vis, imagename=out_root+'.dirty', mask=mask, field='M33*',
          restfreq='1420.40575177MHz', mode='velocity',
          width='1.288km/s', nchan=205, start='-339.104km/s', cell='1.5arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=0,
          threshold='2.0mJy/beam', imagermode='mosaic',
          multiscale=[],
          pbcor=False, interpolation='linear', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79', veltype='radio',
          outframe='LSRK')

if do_clean_1chan:

    os.system('rm -rf '+out_root+'.cent_chan*')

    vis = vis + '.contsub'

    # For multiscale, 1 pixel = 1.5 arcsec

    clean(vis=vis, imagename=out_root+'.cent_chan', field='M33*',
          restfreq='1420.40575177MHz', mode='velocity', nterms=1,
          width='1.288km/s', nchan=1, start='-200km/s', cell='3arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=500,
          threshold='2.0mJy/beam', imagermode='mosaic',
          multiscale=[],
          pbcor=False, interpolation='linear', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79', veltype='radio',
          interactive=True)

if do_clean:

    print 'Making cleaned cube.'

    os.system('rm -rf '+out_root+'.clean')

    mask = None

    vis = vis + '.contsub'

    clean(vis=vis, imagename=out_root+'.clean_lsrk', mask=mask, field='M33*',
          restfreq='1420.40575177MHz', mode='velocity',
          width='1.288km/s', nchan=205, start='-339.104km/s', cell='1.5arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=500,
          threshold='2.0mJy/beam', imagermode='mosaic',
          multiscale=[0, 3, 9, 27, 200],
          pbcor=False, interpolation='linear', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79', veltype='radio',
          outframe='LSRK')

if do_export:

    print "Exporting fits files."

    # Clean cube
    exportfits(imagename=out_root+'.clean.image',
               fitsimage=out_root+'.fits', overwrite=True,
               velocity=True, dropstokes=True)

    # Residual cube
    exportfits(imagename=out_root+'.clean.residual',
               fitsimage=out_root+'_resid.fits', overwrite=True,
               velocity=True, dropstokes=True)

    # Export the primary beam image for the cleaned cube
    exportfits(imagename=out_root+'.clean.flux',
               fitsimage=out_root+'_flux.fits', overwrite=True,
               velocity=True, dropstokes=True)

    # Export the dirty image
    exportfits(imagename=out_root+'.dirty.image',
               fitsimage=out_root+'_dirty.fits', overwrite=True,
               velocity=True, dropstokes=True)
