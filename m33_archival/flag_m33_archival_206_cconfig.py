
'''
Data Flagging for M33 archival VLA data
'''

# Some times with wacky amplitudes

# Bandpass/amp calib
flagdata(vis="M33.ms", timerange='5:25:20~5:25:40')
flagdata(vis="M33.ms", timerange='5:54:20~5:54:40')
flagdata(vis="M33.ms", timerange='8:20:00~8:20:20')
flagdata(vis="M33.ms", timerange='6:23:20~6:23:35')

# Phase calib
flagdata(vis="M33.ms", timerange='4:51:30~4:51:50')
flagdata(vis="M33.ms", timerange='4:58:10~4:58:20')

# P1
flagdata(vis="M33.ms", timerange='6:26:00~6:26:20')

# P5
flagdata(vis="M33.ms", timerange='5:56:40~5:57:00')

