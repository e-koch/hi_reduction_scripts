
vis = "M33_206_B_2.ms"

# SPW 0 just looks awful
flagdata(vis=vis, spw='0')

# Antenna 13 and 15 are bad
flagdata(vis=vis, antenna='13, 15')
