#!/usr/bin/env python
# -----------------------------------------------------------------------------
# RATIOS
# -----------------------------------------------------------------------------

import re
import asciitable as at
from numpy import *


fname = "schedule.txt"

male = at.read( "male_uniq.csv", names=[ "name", "nm" ],
    comment='#', guess=False, Reader=at.NoHeader, delimiter="," )
female = at.read( "female_uniq.csv", names=[ "name", "nf" ],
    comment='#', guess=False, Reader=at.NoHeader, delimiter="," )
unisex = at.read( "unisex_uniq.csv", names=[ "name", "nf",
    "nm" ], comment='#', guess=False, Reader=at.NoHeader )


def get_gender( name ):
    
    wm = where( male.name == name )
    wf = where( female.name == name )
    if not size( wm ) and not size( wf ): gender= "x"
    elif size( wm ) == 0: gender = "m"
    elif size( wf ) == 0: gender = "f"
    elif male[wm].nm > female[wf].nf: gender = "m"
    elif male[wm].nm < female[wf].nf: gender = "f"
    else: gender = "e"
    
    if gender == "e": print "OH NO!"
    
    return gender

gl = ""

f = open( fname, "r" )
lines = f.readlines()
for i in range( size( lines ) ):
    
    line = lines[i]
    
    # word = '102. 01D. Toward a precise determination of the neutral gas fraction at z~7 using the Lyman alpha fraction test'
    regexp1 = re.compile( r'[0-9][0-9][0-9][.][ ][0-9][0-9][.][ ]' )
    regexp2 = re.compile( r'[0-9][0-9][0-9][.][ ][0-9][0-9][D][.][ ]' )
    regexp3 = re.compile( r'[0-9][0-9][0-9][.][ ]' )
    
    if regexp1.search( line ) is not None:
        stat = "talk"
    elif regexp2.search( line ) is not None:
        stat = "talk"
    elif regexp3.search( line ) is not None:
        stat = "session"
    else: stat = ""
    
    if stat == "talk":
        speaker = lines[i+1].split( ";" )[0].strip().split()[0]
        gender = get_gender( speaker )
        gl = gl + gender
    
    if stat == "session":
        
        if gl: print session, chair_gender, gl
        gl = ""
        
        session = line[:3]
        chair = lines[i+1].split( ":" )[1].split( "(" )[0].strip().split()[0]
        
        chair_gender = get_gender( chair )


f.close()
