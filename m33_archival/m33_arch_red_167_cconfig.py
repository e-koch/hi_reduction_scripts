
'''

Import archival VLA data and do stuff...

'''

import os

from tasks import *
from taskinit import *
import casac


# Load in functions from vla_heracles
execfile(
    "/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/vla_heracles/akl_21cm.py")
execfile(
    "/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/vla_heracles/akl_21cm_calib.py")
execfile(
    "/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/vla_heracles/akl_21cm_suggest_refant.py")
execfile(
    '/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/vla_heracles/akl_21cm_autoflag.py')
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CONTROL FLOW
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
do_load = True
do_flag = True
do_calib = True
do_inspectcal = True
do_inspect = False
do_split = False

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DEFINITIONS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%


out_root = 'M33_167_C'
vis = 'M33_167_C.ms'

raw_files = ["AT206_7", "AT206_8", "AT206_9"]

if do_load:

    # Because the data uses one standard for all its calibrations,and since
    # the archival data does not have specified scan intents, we need to be
    # 'inventive'. For the life of me, I can't figure out how to change the
    # scan intents and have them read in properly.
    # SO I'm going to split the data set up, change the field names of the
    # standard, then concatenate it all back together. Maybe this will work

    import_21cm(out_root=out_root,
                raw_files=raw_files)

    orig_vis = "M33_167_C.ms"

    split(vis=orig_vis, outputvis="M33_spl_ph.ms",
          scan='3, 4, 8, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25,\
                27, 28, 30, 31, 33', field='0')

    split(vis=orig_vis, outputvis="M33_spl_bp_amp.ms", scan='1', field='0')

    split(vis=orig_vis, outputvis="M33_spl_src.ms",
          field='1, 2, 3, 4')

    # Change the field names
    tb.open("M33_spl_bp_amp.ms/FIELD", nomodify=False)
    st = tb.selectrows(0)
    st.putcol("NAME", "0134+329_bp_amp")
    st.done()
    tb.close()
    tb.open("M33_spl_bp_amp.ms/SOURCE", nomodify=False)
    st = tb.selectrows(0)
    st.putcol("NAME", "0134+329_bp_amp")
    st.putcol("SOURCE_ID", 4)
    st.done()
    tb.close()

    tb.open("M33_spl_ph.ms/FIELD", nomodify=False)
    st = tb.selectrows(0)
    st.putcol("NAME", "0134+329_ph")
    st.done()
    tb.close()
    tb.open("M33_spl_ph.ms/SOURCE", nomodify=False)
    st = tb.selectrows(0)
    st.putcol("NAME", "0134+329_ph")
    st.done()
    tb.close()

    # Set respectname=True in order to keep the calibration fields
    # as separate
    concat(vis=["M33_spl_bp_amp.ms", "M33_spl_ph.ms", "M33_spl_src.ms"],
           concatvis=vis, respectname=True)

    # Now get rid of the split up data
    os.system("rm -rf M33_spl*")

if do_flag:
    # Does autoflagging of general problem areas, including edge channels
    autoflag_21cm(out_root='M33')  # , edge_str="0~1:0~20;225~254", reset=True)

    # execfile(
    #     "/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/m33_archival/flag_m33_archival_206_cband.py")

if do_calib:

    ref_ant = suggest_refant(vis=vis)

    # Now run the calibration on the remade data set

    calib_21cm(out_root=out_root, source="M33P*",
               fluxcal="0134+329_bp_amp",
               bpcal="0134+329_bp_amp", phasecal="0134+329_ph",
               ref_ant=ref_ant)

if do_inspectcal:

    print ""
    print "Inspecting Calibration Tables for " + vis
    print ""

    # get the list of antennas
    tb.open(vis+"/ANTENNA")
    ant_list = tb.getcol("NAME")
    tb.close()

    # get the number of spws
    tb.open(vis+"/SPECTRAL_WINDOW")
    spw_list_in = tb.getcol("NAME")
    tb.close()
    spw_list = []
    for i in range(len(spw_list_in)):
        spw_list.append(str(i))

    # Make some plots!
    caltable = out_root + ".bpcal"
    outdir = caltable + ".plots/"
    os.system("rm -rf " + outdir)
    os.system("mkdir " + outdir)
    print "Phase/Amp vs. frequency solution"
    for ant in ant_list:
        plotcal(caltable=caltable,
                xaxis="freq",
                yaxis="phase",
                iteration="antenna",
                plotrange=[0, 0, -180, 180],
                plotsymbol='o', subplot=111,
                antenna=ant,
                figfile=outdir + "bphase_" + ant + ".png")
        plotcal(caltable=caltable,
                xaxis="freq",
                yaxis="amp",
                iteration="antenna",
                plotrange=[0, 0, 0, 0],
                plotsymbol='o', subplot=111,
                antenna=ant,
                figfile=outdir + "bpamp_" + ant + ".png")

    for spw in spw_list:
        plotcal(caltable=caltable,
                xaxis="chan",
                yaxis="amp",
                iteration="spw",
                plotrange=[0, 0, 0, 0],
                plotsymbol='o', subplot=111,
                spw=spw,
                figfile=outdir + "amp_vs_chan_spw" + spw + ".png")

    caltable = out_root + ".scanphase.gcal"
    outdir = caltable + ".plots/"
    os.system("rm -rf " + outdir)
    os.system("mkdir " + outdir)
    print "Phase vs. time"
    for ant in ant_list:
        plotcal(caltable=caltable,
                xaxis="time",
                yaxis="phase",
                iteration="antenna",
                plotrange=[0, 0, 0, 0],
                plotsymbol='o', subplot=111,
                antenna=ant,
                figfile=outdir + "phase_" + ant + ".png")

    caltable = out_root + ".fcal"
    outdir = caltable + ".plots/"
    os.system("rm -rf " + outdir)
    os.system("mkdir " + outdir)
    print "Amplitude vs. time"
    for ant in ant_list:
        plotcal(caltable=caltable,
                xaxis="time",
                yaxis="amp",
                iteration="antenna",
                plotrange=[0, 0, 0, 0],
                plotsymbol='o', subplot=111,
                antenna=ant,
                figfile=outdir + "flux_" + ant + ".png")

if do_inspect:

    fluxcal = "0134+329_bp_amp"
    phasecal = "0134+329_ph"
    bpcal = "0134+329_bp_amp"

    cals = fluxcal + ", " + bpcal + ", " + phasecal

    print ""
    print "Inspecting Data for "+vis
    print ""
    plotms(vis=vis,
           iteraxis="field",
           xaxis="frequency",
           yaxis="amp",
           avgtime="1e8",
           averagedata=True,
           avgscan=True,
           ydatacolumn="corrected",
           field=cals)
    print "Amplitude-frequency"
    ch = raw_input("Hit a key to continue.")

    plotms(vis=vis,
           xaxis="uvdist",
           yaxis="amp",
           ydatacolumn="corrected",
           avgchannel="256",
           avgtime="1e8",
           averagedata=True,
           field=phasecal)
    print "Amplitude-uvdist"
    ch = raw_input("Hit a key to continue.")

    plotms(vis=vis,
           xaxis="time",
           yaxis="amp",
           ydatacolumn="corrected",
           avgchannel="256",
           averagedata=True,
           coloraxis="field")
    print "Amplitude-time"
    ch = raw_input("Hit a key to continue.")

# Split off the corrected source fields

if do_split:

    print 'Splitting off calibrated data'

    os.system('rm -rf '+out_root+'.split')

    split(vis=vis, outputvis=out_root+".split", field="M33*",
          datacolumn='corrected', keepflags=False)

