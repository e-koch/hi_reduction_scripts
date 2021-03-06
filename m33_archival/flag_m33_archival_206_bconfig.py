
'''
Data Flagging for M33 archival VLA data - B config
'''

import sys

from tasks import *
from taskinit import *
import casac

set_num = int(sys.argv[1])

vis = "M33_206_B_"+str(set_num)

if set_num == 1:
    flagdata(vis=vis, antenna='26')
elif set_num == 2:
    flagdata(vis=vis, spw='0')
    flagdata(vis=vis, antenna='13, 15')

elif set_num == 3:
    flagdata(vis=vis, antenna='28')
    # flagdata(vis=vis, spw='0', antenna='5')

elif set_num == 4:
    flagdata(vis=vis, antenna='16')

elif set_num == 5:
    pass

elif set_num == 6:
    pass

else:
    print("Yousa needsa to changsa your inputsa.")

# Some times with wacky amplitudes

# Bandpass/amp calib
# flagdata(vis="M33.ms", timerange='5:25:20~5:25:40')
# flagdata(vis="M33.ms", timerange='5:54:20~5:54:40')
# flagdata(vis="M33.ms", timerange='8:20:00~8:20:20')
# flagdata(vis="M33.ms", timerange='6:23:20~6:23:35')

# # Phase calib
# flagdata(vis="M33.ms", timerange='4:51:30~4:51:50')
# flagdata(vis="M33.ms", timerange='4:58:10~4:58:20')

# # P1
# flagdata(vis="M33.ms", timerange='6:26:00~6:26:20')

# # P5
# flagdata(vis="M33.ms", timerange='5:56:40~5:57:00')

