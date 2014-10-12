
'''
M33 Archival VLA Data
Make the cube
'''

import os

from tasks import *
from taskinit import *
import casac

do_cvel = False
do_plotcontsub = False
do_contsub = False
do_plotsub = False
do_image = True
do_clean = True
do_export = False

vis = "M33.split"
out_root = 'M33'

if do_cvel:

    os.system('rm -rf '+out_root+'.cvel')
    cvel(vis=vis, outputvis=out_root+'.cvel', mode='velocity',
         nchan=-1, start=0, width=1, restfreq='1420.40575177MHz',
         outfram='LSRK')

if do_plotcontsub:

    print "Plotting amp. vs. chan"

    plotms(vis=vis, field="M33*", xaxis='chan', yaxis='amp', avgtime='1e8s',
           avgscan=True, avgbaseline=True)
    wait = raw_input("Continue?")

if do_contsub:

    print "Subtracting continuum."

    os.system('rm -rf '+out_root+'.contsub')

    uvcontsub(vis=vis, field="M33*", combine='spw', solint='int', fitorder=0)

if do_image:

    vis = vis + '.contsub'

    # First creates a dirty cube to examine

    print "Making dirty cube."

    os.system('rm -rf '+out_root+'.dirty*')

    clean(vis=vis, imagename=out_root+'.dirty', restfreq='1420.40575177MHz',
          mode='channel', width=1, nchan=256, start=1, cell='3arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=0,
          pbcor=False, interpolation='cubic', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79')

if do_clean:

    print 'Making cleaned cube.'

    os.system('rm -rf '+out_root+'.clean')

    mask = None

    vis = vis + '.contsub'

    clean(vis=vis, imagename=out_root+'.test', mask=mask, field='M33*',
          restfreq='1420.40575177MHz', mode='channel',
          width=1, nchan=1, start=128, cell='3arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=7000,
          threshold='0.0mJy/beam', imagermode='mosaic', multiscale=[],
          pbcor=False, interpolation='cubic', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79')

    clean(vis=vis, imagename=out_root+'.clean', mask=mask, field='M33*',
          restfreq='1420.40575177MHz', mode='channel',
          width=1, nchan=256, start=1, cell='3arcsec',
          imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=7000,
          threshold='0.0mJy/beam', imagermode='mosaic', multiscale=[],
          pbcor=False, interpolation='cubic', usescratch=True,
          phasecenter='J2000 01h33m50.904 +30d39m35.79')

    # clean(vis="M33.ms", field='0137+331*', imagename=out_root+'.calib.clean', mask=mask,
    #       restfreq='1420.40575177MHz', mode='channel',
    #       width=1, nchan=1, start=128, cell='4arcsec',
    #       imsize=[2048, 2048], weighting='briggs', robust=0.0, niter=5000,
    #       threshold='0.0mJy/beam', imagermode='mosaic', multiscale=[],
    #       pbcor=False, interpolation='cubic', usescratch=True)

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
