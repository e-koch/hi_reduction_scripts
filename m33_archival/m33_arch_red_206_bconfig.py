
'''

Import archival VLA data and do stuff...

'''

import os
import glob

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
do_load = False
do_flag = False
do_calib = False
do_inspectcal = False
do_inspect = False
do_split = True

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DEFINITIONS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%


out_root = 'M33_206_B_'

raw_files = glob.glob("AT206_*")


# Split into tracks
raw_splits = [raw_files[:7], raw_files[7:15], raw_files[15:23],
              raw_files[23:31], raw_files[31:38], raw_files[38:]]

phase_fields = ['3, 6, 8, 10, 13, 15, 17, 20, 22, 24, \
                 27, 29, 31, 32, 34, 36, 39, 41, 43',
                '3, 4, 6, 8, 11, 13, 15, 18, 20, 22, 25, \
                 27, 30, 32, 34, 37, 39, 41, 44',
                '2, 4, 6, 9, 11, 13, 16, 18, 20, 23, \
                 25, 28, 30 ,32, 35, 37, 39, 42, 44',
                '4, 6, 8, 11, 13, 16, 18, 20, 23, 25, \
                 27, 30, 32, 34, 37, 39, 42, 44',
                '3, 5, 6, 8, 10, 12, 13, 15, 17, 20, \
                 22, 24, 27, 29, 31, 34, 36, 39, 41, 43',
                '4, 6, 8, 11, 13, 16, 18, 20, 23, 25, 27, \
                 30, 32, 34, 36, 38, 41, 43']

if do_load:

    # Because the data uses one standard for all its calibrations,and since
    # the archival data does not have specified scan intents, we need to be
    # 'inventive'. For the life of me, I can't figure out how to change the
    # scan intents and have them read in properly.
    # SO I'm going to split the data set up, change the field names of the
    # standard, then concatenate it all back together. Maybe this will work

    pre_loaded = False

    for i, raws in enumerate(raw_splits):

        print "Importing %s/%s" % (i+1, len(raw_splits))

        if not pre_loaded:
            import_21cm(out_root="M33_206_B_orig_"+str(i+1),
                        raw_files=raws)

        orig_vis = "M33_206_B_orig_"+str(i+1)+".ms"

        split(vis=orig_vis, outputvis="M33_206_B_spl_ph.ms",
              scan=phase_fields[i],
              field='0')

        split(vis=orig_vis, outputvis="M33_206_B_spl_bp_amp.ms",
              scan='1', field='0')

        split(vis=orig_vis, outputvis="M33_206_B_spl_src.ms",
              field='1, 2, 3, 4, 5, 6')

        # Change the field names
        tb.open("M33_206_B_spl_bp_amp.ms/FIELD", nomodify=False)
        st = tb.selectrows(0)
        st.putcol("NAME", "0137+331_bp_amp")
        st.done()
        tb.close()
        tb.open("M33_206_B_spl_bp_amp.ms/SOURCE", nomodify=False)
        st = tb.selectrows(0)
        st.putcol("NAME", "0137+331_bp_amp")
        st.putcol("SOURCE_ID", 4)
        st.done()
        tb.close()

        tb.open("M33_206_B_spl_ph.ms/FIELD", nomodify=False)
        st = tb.selectrows(0)
        st.putcol("NAME", "0137+331_ph")
        st.done()
        tb.close()
        tb.open("M33_206_B_spl_ph.ms/SOURCE", nomodify=False)
        st = tb.selectrows(0)
        st.putcol("NAME", "0137+331_ph")
        st.done()
        tb.close()

        # Set respectname=True in order to keep the calibration fields
        # as separate
        concat(vis=["M33_206_B_spl_bp_amp.ms",
                    "M33_206_B_spl_ph.ms",
                    "M33_206_B_spl_src.ms"],
               concatvis=out_root+str(i+1)+".ms", respectname=True)

        # Now get rid of the split up data
        os.system("rm -rf M33_206_B_spl*")

if do_flag:

    for i in range(1, 7):

        if i == 2:
            continue

        # Does autoflagging of general problem areas, including edge channels
        autoflag_21cm(out_root=out_root+str(i),
                      edge_str="0~1:0~20;225~254",
                      reset=True)

        execfile(
            "/Users/eric/Dropbox/code_development/m33_code/hi_reduction_scripts/m33_archival/flags_206_B/flag_m33_206_b_"+str(i)+".py")

if do_calib:

    for i in range(1, 7):

        if i == 2:
            continue

        vis = out_root + str(i) + ".ms"

        ref_ant = suggest_refant(vis=vis)

    # Now run the calibration on the remade data set

        calib_21cm(out_root=out_root+str(i), source="M33P*",
                   fluxcal="0137+331_bp_amp",
                   bpcal="0137+331_bp_amp", phasecal="0137+331_ph",
                   ref_ant=ref_ant)

if do_inspectcal:

    for i in range(1, 7):

        if i == 2:
            continue

        print ""
        print "Inspecting Calibration Tables for " + out_root + str(i)
        print ""

        interactive = False

        vis = out_root + str(i) + ".ms"

        # get the list of antennas
        tb.open(vis+"/ANTENNA")
        ant_list = tb.getcol("NAME")
        tb.close()

        # get the number of spws
        tb.open(vis+"/SPECTRAL_WINDOW")
        spw_list_in = tb.getcol("NAME")
        tb.close()
        spw_list = []
        for j in range(len(spw_list_in)):
            spw_list.append(str(j))

        # Make some plots!
        caltable = out_root + str(i) + ".bpcal"
        outdir = caltable + str(i) + ".plots/"
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
            if interactive:
                raw_input("Continue?")
            plotcal(caltable=caltable,
                    xaxis="freq",
                    yaxis="amp",
                    iteration="antenna",
                    plotrange=[0, 0, 0, 0],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir + "bpamp_" + ant + ".png")
            if interactive:
                raw_input("Continue?")

        for spw in spw_list:
            plotcal(caltable=caltable,
                    xaxis="chan",
                    yaxis="amp",
                    iteration="spw",
                    plotrange=[0, 0, 0, 0],
                    plotsymbol='o', subplot=111,
                    spw=spw,
                    figfile=outdir + "amp_vs_chan_spw" + spw + ".png")
            if interactive:
                raw_input("Continue?")

        caltable = out_root + str(i) + ".scanphase.gcal"
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
            if interactive:
                raw_input("Continue?")

        caltable = out_root + str(i) + ".fcal"
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
            if interactive:
                raw_input("Continue?")

if do_inspect:

    for i in range(1, 7):

        if i == 2:
            continue

        vis = out_root + str(i) + ".ms"

        fluxcal = "0137+331_bp_amp"
        phasecal = "0137+331_ph"
        bpcal = "0137+331_bp_amp"

        cals = fluxcal + ", " + bpcal + ", " + phasecal

        print ""
        print "Inspecting Data for " + out_root + str(i)
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
               iteraxis="field",
               xaxis="frequency",
               yaxis="phase",
               avgtime="1e8",
               averagedata=True,
               avgscan=True,
               ydatacolumn="corrected",
               field=cals)
        print "Phase-frequency"
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

    for i in range(1, 7):

        if i == 2:
            continue

        print 'Splitting off calibrated data'

        os.system('rm -rf '+out_root+str(i)+'.split')

        split(vis=out_root+str(i)+".ms",
              outputvis=out_root+str(i)+".split", field="M33*",
              datacolumn='corrected', keepflags=True)

    print 'Now combining all reduced data into one set.'

    # If you don't delete, it concatenates onto the existing one.
    os.system('rm -rf M33_bconfig_all.split')

    concat(vis=glob.glob("M33*.split"), concatvis='M33_bconfig_all.split',
           timesort=True, freqtol='10MHz')
