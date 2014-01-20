#!/usr/bin/env python
# -----------------------------------------------------------------------------
# PLOT_SPEAKERS
# speaker gender histograms for all talks
# -----------------------------------------------------------------------------

import astropy.io.ascii as ascii
from matplotlib.pyplot import *
from numpy import *


# set up plotting
rc( "font", family="serif" )
rc( "text", usetex=True )
rc( "xtick", labelsize=10 )
rc( "ytick", labelsize=10 )
rc( "axes", labelsize=10, titlesize=14 )
rc( "legend", fontsize=9 )
rc( "patch", ec="None" )


# read talk gender info
talk = ascii.read( "data/talks.dat" )

# convert f/m into numbers for histogram plotting
gspeaker = zeros( size( talk ) )
gspeaker[ where( talk["speaker"] == "f" ) ] = 1
gspeaker[ where( talk["speaker"] == "m" ) ] = 2

# number of female and male chairs
nf = size( where( talk["speaker"] == "f" ) )
nm = size( where( talk["speaker"] == "m" ) )
ymax = ceil( max( nf, nm ) * 1.25 / 10. ) * 10.

# percentages
pf = 100. * nf / size( talk )
pm = 100. * nm / size( talk )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "All Speakers" )
xlim( 0.4, 2.6 )
ylim( 0, ymax )
xticks( arange(2)+1, ( "Female", "Male" ) )
ylabel( "Number" )

# histograms
hist( gspeaker, bins=1, range=(0.65,1.35), color="green", alpha=0.75 )
hist( gspeaker, bins=1, range=(1.65,2.35), color="blue", alpha=0.75 )

# print f/m numbers and percentages
text( 1., nf + 0.1 * ymax, "{:}".format( nf ), ha="center", size=10 )
text( 1., nf + 0.02 * ymax, "({:.1f}\%)".format( pf ), ha="center", size=10 )
text( 2., nm + 0.1 * ymax, "{:}".format( nm ), ha="center", size=10 )
text( 2., nm + 0.02 * ymax, "({:.1f}\%)".format( pm ), ha="center", size=10 )

# show and save
show()
savefig( "graph/speakers.pdf" )
savefig( "graph/speakers.png" )
