#!/usr/bin/env python
# -----------------------------------------------------------------------------
# CHAIRS_QUESTIONS
# question gender histograms split by chair gender
# -----------------------------------------------------------------------------

import astropy.io.ascii as ascii
from matplotlib.pyplot import *
from numpy import *
import string


# read data
sess = ascii.read( "data/sessions.dat" )
talk = ascii.read( "data/talks.dat" )
data = ascii.read( "data/questions.dat" )


# make array to store chair/question genders
qs = array( [ "" ] * 1000 ).astype( "S2" )
count = 0

for d in data:
    
    wh = where( talk["id"] == d["talk"] )
    
    if size( wh ):
        
        match = talk[wh]["speaker"] == string.lower( d["speaker"] )
        
        if match:
            
            chair = sess[ sess["id"] == int( d["talk"] ) ]["chair"][0]
            for q in d["questions"]:
                qs[count] = "{:}{:}".format( chair, string.lower( q ) )
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
qq[ where( qs == "ff" ) ] = 0.8
qq[ where( qs == "fm" ) ] = 1.2
qq[ where( qs == "mf" ) ] = 1.8
qq[ where( qs == "mm" ) ] = 2.2

# number of female and male chairs/questions
nff = size( where( qs == "ff" ) )
nfm = size( where( qs == "fm" ) )
nmf = size( where( qs == "mf" ) )
nmm = size( where( qs == "mm" ) )
ymax = ceil( max( nff, nfm, nmf, nmm ) * 1.25 / 10. ) * 10.

# percentages
pff = 100. * nff / ( nff + nfm )
pfm = 100. * nfm / ( nff + nfm )
pmf = 100. * nmf / ( nmf + nmm )
pmm = 100. * nmm / ( nmf + nmm )

# set up figure
fig = figure( figsize=( 4, 3 ) )
fig.subplots_adjust( left=0.15, bottom=0.09, top=0.89, right=0.97 )
title( "Chairs | Questions" )
xlim( 0.4, 2.6 )
ylim( 0, ymax )
xticks( unique(qq), ( "FC FQ", "FC MQ", "MC FQ", "MC MQ" ) )
ylabel( "Number" )

# histograms
hist( qq, bins=1, range=(0.6,1.0), color="g", alpha=0.75 )
hist( qq, bins=1, range=(1.0,1.4), color="b", alpha=0.75 )
hist( qq, bins=1, range=(1.6,2.0), color="g", alpha=0.75 )
hist( qq, bins=1, range=(2.0,2.4), color="b", alpha=0.75 )

# print f/m numbers and percentages
text( 0.8, nff + 0.1 * ymax, "{:}".format( nff ), ha="center", size=10 )
text( 1.2, nfm + 0.1 * ymax, "{:}".format( nfm ), ha="center", size=10 )
text( 1.8, nmf + 0.1 * ymax, "{:}".format( nmf ), ha="center", size=10 )
text( 2.2, nmm + 0.1 * ymax, "{:}".format( nmm ), ha="center", size=10 )

text( 0.8, nff + 0.02 * ymax, "({:.1f}\%)".format( pff ), ha="center", size=10 )
text( 1.2, nfm + 0.02 * ymax, "({:.1f}\%)".format( pfm ), ha="center", size=10 )
text( 1.8, nmf + 0.02 * ymax, "({:.1f}\%)".format( pmf ), ha="center", size=10 )
text( 2.2, nmm + 0.02 * ymax, "({:.1f}\%)".format( pmm ), ha="center", size=10 )

# show and save
show()
savefig( "graph/chairs_questions.pdf" )
savefig( "graph/chairs_questions.png" )
