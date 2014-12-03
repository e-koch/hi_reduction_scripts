
vis = "M33_206_B_4.ms"


# Antenna 20 is bad
flagdata(vis=vis, antenna='VA20')

# Antenna 16 has no gain/phase solution
flagdata(vis=vis, antenna='VA16')

