#!/usr/bin/env python
# -----------------------------------------------------------------------------
# MAKE_PLOTS
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


# -----------------------------------------------------------------------------


# chair gender histograms for all sessions


# read session gender info
sess = ascii.read( "data/sessions.dat" )

# convert f/m into numbers for histogram plotting
gchair = zeros( size( sess ) )
gchair[ where( sess["chair"] == "f" ) ] = 1
gchair[ where( sess["chair"] == "m" ) ] = 2

# number of female and male chairs
nf = size( where( sess["chair"] == "f" ) )
nm = size( where( sess["chair"] == "m" ) )

# percentages
pf = 100. * nf / size( sess )
pm = 100. * nm / size( sess )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "Session Chairs" )
xlim( 0.4, 2.6 )
xticks( arange(2)+1, ( "Female", "Male" ) )
ylabel( "Number" )

# histograms
hist( gchair, bins=1, range=(0.65,1.35), color="green", alpha=0.75 )
hist( gchair, bins=1, range=(1.65,2.35), color="blue", alpha=0.75 )

# print f/m numbers and percentages
text( 1., nf - 10, "{:}".format( nf ), ha="center" )
text( 1., nf - 20, "({:.1f}\%)".format( pf ), ha="center" )
text( 2., nm - 10, "{:}".format( nm ), ha="center" )
text( 2., nm - 20, "({:.1f}\%)".format( pm ), ha="center" )

# show and save
show()
savefig( "graph/chairs.pdf" )
savefig( "graph/chairs.png" )


# -----------------------------------------------------------------------------


# speaker gender histograms for all talks


# read talk gender info
talk = ascii.read( "data/talks.dat" )

# convert f/m into numbers for histogram plotting
gspeaker = zeros( size( talk ) )
gspeaker[ where( talk["speaker"] == "f" ) ] = 1
gspeaker[ where( talk["speaker"] == "m" ) ] = 2

# number of female and male chairs
nf = size( where( talk["speaker"] == "f" ) )
nm = size( where( talk["speaker"] == "m" ) )

# percentages
pf = 100. * nf / size( talk )
pm = 100. * nm / size( talk )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "All Speakers" )
xlim( 0.4, 2.6 )
xticks( arange(2)+1, ( "Female", "Male" ) )
ylabel( "Number" )

# histograms
hist( gspeaker, bins=1, range=(0.65,1.35), color="green", alpha=0.75 )
hist( gspeaker, bins=1, range=(1.65,2.35), color="blue", alpha=0.75 )

# print f/m numbers and percentages
text( 1., nf - 60, "{:}".format( nf ), ha="center" )
text( 1., nf - 120, "({:.1f}\%)".format( pf ), ha="center" )
text( 2., nm - 60, "{:}".format( nm ), ha="center" )
text( 2., nm - 120, "({:.1f}\%)".format( pm ), ha="center" )

# show and save
show()
savefig( "graph/speakers.pdf" )
savefig( "graph/speakers.png" )
