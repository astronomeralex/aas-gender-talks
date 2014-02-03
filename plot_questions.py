#!/usr/bin/env python
# -----------------------------------------------------------------------------
# PLOT_QUESTIONS
# question gender histograms for all talks
# -----------------------------------------------------------------------------

import astropy.io.ascii as ascii
from matplotlib.pyplot import *
from numpy import *
import string


# read data
sess = ascii.read( "data/sessions.dat" )
talk = ascii.read( "data/talks.dat" )
data = ascii.read( "data/questions.dat" )


# make array to store question genders
qs = array( [ "" ] * 1000 ).astype( "S2" )
count = 0

for d in data:
    
    wh = where( talk["id"] == d["talk"] )
    
    if size( wh ):
        
        match = talk[wh]["speaker"] == string.lower( d["speaker"] )
        
        if match:
            
            for q in d["questions"]:
                qs[count] = "{:}".format( string.lower( q ) )
                count += 1

# select non-null values
qs = qs[qs != ""]


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
qq = zeros( qs.size )
qq[ where( qs == "f" ) ] = 1
qq[ where( qs == "m" ) ] = 2

# number of female and male chairs/questions
nf = size( where( qs == "f" ) )
nm = size( where( qs == "m" ) )
ymax = ceil( max( nf, nm ) * 1.25 / 10. ) * 10.

# percentages
pf = 100. * nf / ( nf + nm )
pm = 100. * nm  / ( nf + nm )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "Questions" )
xlim( 0.4, 2.6 )
ylim( 0, ymax )
xticks( arange(2)+1, ( "Female", "Male" ) )
ylabel( "Number" )

# histograms
hist( qq, bins=1, range=(0.65,1.35), color="g", alpha=0.75 )
hist( qq, bins=1, range=(1.65,2.35), color="b", alpha=0.75 )

# print f/m numbers and percentages
text( 1., nf + 0.1 * ymax, "{:}".format( nf ), ha="center", size=10 )
text( 1., nf + 0.02 * ymax, "({:.1f}\%)".format( pf ), ha="center", size=10 )
text( 2., nm + 0.1 * ymax, "{:}".format( nm ), ha="center", size=10 )
text( 2., nm + 0.02 * ymax, "({:.1f}\%)".format( pm ), ha="center", size=10 )

# show and save
show()
savefig( "graph/questions.pdf" )
savefig( "graph/questions.png" )
