
'''
Create scan intents for archival VLA data
'''

from tasks import *
from taskinit import *
import casac


def add_intents(out_root=None,
                intents=["CALIBRATE_PHASE", "POINTING", "POINTING",
                         "CALIBRATE_BANDPASS, CALIBRATE_AMPLITUDE",
                         "POINTING"],
                verbose=False):
    '''
    Add scan intents for archival VLA data. Needed when the same source is
    used for different calibrations.
    '''

    vis = out_root + ".ms"

    # Open the appropriate table
    tb.open(vis+"/STATE", nomodify=False)

    assert "OBS_MODE" in tb.colnames()

    # Add rows on
    tb.addrows(len(intents))
    tb.putcol("OBS_MODE", intents)

    if verbose:
        print(tb.getcol("OBS_MODE"))

    tb.close()

    return
