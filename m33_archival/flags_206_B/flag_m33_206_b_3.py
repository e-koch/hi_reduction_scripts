
vis = "M33_206_B_3.ms"

# Antenna 5 spw 0 is bad
flagdata(vis=vis, antenna='VA05', spw='0')

# Antenna 12 is bad
flagdata(vis=vis, antenna='VA20')

# Antenna 28 has no gain/phase solution
flagdata(vis=vis, antenna='VA28')
