#!/usr/bin/env python
# -----------------------------------------------------------------------------
# PLOT_SPEAKERS_DATA
# speaker gender histograms for talks for which we have data
# -----------------------------------------------------------------------------

import astropy.io.ascii as ascii
from matplotlib.pyplot import *
from numpy import *
import string


# read data
sess = ascii.read( "data/sessions.dat" )
talk = ascii.read( "data/talks.dat" )
data = ascii.read( "data/questions.dat" )


# clean out any data where speaker gender does not match schedule
index = array( [] ).astype( "<i8" )

for i in range( size( data ) ):
    
    wh = where( talk["id"] == data[i]["talk"] )
    match = talk[wh]["speaker"] == string.lower( data[i]["speaker"] )
    
    if match:
        
        index = append( index, i )

data = data[index]


# -----------------------------------------------------------------------------


# set up plotting
rc( "font", family="serif" )
rc( "text", usetex=True )
rc( "xtick", labelsize=10 )
rc( "ytick", labelsize=10 )
rc( "axes", labelsize=10, titlesize=14 )
rc( "legend", fontsize=9 )
rc( "patch", ec="None" )


# convert f/m into numbers for histogram plotting
gspeaker = zeros( size( data ) )
gspeaker[ where( data["speaker"] == "F" ) ] = 1
gspeaker[ where( data["speaker"] == "M" ) ] = 2

# number of female and male speakers
nf = size( where( data["speaker"] == "F" ) )
nm = size( where( data["speaker"] == "M" ) )
ymax = ceil( max( nf, nm ) * 1.25 / 10. ) * 10.

# percentages
pf = 100. * nf / size( data )
pm = 100. * nm / size( data )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "Data Speakers" )
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
savefig( "graph/speakers_data.pdf" )
savefig( "graph/speakers_data.png" )
