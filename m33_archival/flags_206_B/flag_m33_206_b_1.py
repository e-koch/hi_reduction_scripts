
vis = "M33_206_B_1.ms"

# Antenna 5 spw 0 is bad
flagdata(vis=vis, antenna='VA05', spw='0')

# Antenna 20 has no gain/phase solution
flagdata(vis=vis, antenna='VA20')

# Antenna 13 is missing gain/phase for half the track
flagdata(vis=vis, antenna='VA13')
