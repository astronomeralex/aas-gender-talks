#!/usr/bin/env python
# -----------------------------------------------------------------------------
# GENDER_FROM_SCHEDULE
#   Gets session/talk numbers and chair/speaker genders from schedule and
#   writes output to file.
# -----------------------------------------------------------------------------

import re
import astropy.io.ascii as ascii
from numpy import *
from numpy.core.records import fromarrays as recinit


# read in name lists
male = ascii.read( "male_uniq.csv", names=[ "name", "nm" ], comment='#' )
female = ascii.read( "female_uniq.csv", names=[ "name", "nf" ], comment='#' )
unisex = ascii.read( "unisex_uniq.csv", names=[ "name", "nf", "nm" ], comment='#' )
extras = ascii.read( "extra_names.csv" )

# get gender by name
def get_gender( name ):
    
    # find name in male and female lists
    wm = where( male["name"] == name )[0]
    wf = where( female["name"] == name )[0]
    
    if not wm and not wf:                                   # name not found
        gender= "x"
        wh = where( extras["name"] == name )
        if extras[wh]["gender"] == "m" or extras[wh]["gender"] == "f":
            gender = extras[wh]["gender"]
    elif not wf: gender = "m"                               # only in male
    elif not wm: gender = "f"                               # only in female
    elif male[wm]["nm"] > female[wf]["nf"]: gender = "m"    # both, more male
    elif male[wm]["nm"] < female[wf]["nf"]: gender = "f"    # both, more female
    else: gender = "e"                                      # error
    
    # want to highlight if an error happens so we can check it out
    if gender == "e": print "OH NO!"
    
    return gender




# make recarray for session data
nn = 200
zz = zeros( nn ).astype( int )
ss = array( [ "" ] * nn ).astype( "S25" )
aa = [ zz ] + [ ss ]
sess = recinit( aa, names="id, chair" )

# make recarray for talk data
nn = 2000
zz = zeros( nn )
ss = array( [ "" ] * nn ).astype( "S25" )
aa = [ zz ] + [ ss ]
talk = recinit( aa, names="id, speaker" )

# some setup stuff
scount = 0
tcount = 0
withdrawn = False
nw = 0

# read from schedule file
fname = "data/schedule.txt"
f = open( fname, "r" )
lines = f.readlines()
for i in range( size( lines ) ):
    
    line = lines[i]
    
    # this is what a five minute talk looks like
    re_reg = re.compile( r'[0-9][0-9][0-9][.][ ][0-9][0-9][.][ ]' )
    
    # this is what a disseration talk looks like
    re_dis = re.compile( r'[0-9][0-9][0-9][.][ ][0-9][0-9][D][.][ ]' )
    
    # this is what a session looks like
    re_ses = re.compile( r'[0-9][0-9][0-9][.][ ]' )
    
    # check for withdrawl - I don't actually do anything with this yet
    if line.strip() == "This presentation has been withdrawn. Withdrawn":
        withdrawn = True
    
    # check if line is a session or a talk
    if re_reg.search( line ) is not None or re_dis.search( line ) is not None:
        stat = "talk"
    elif re_ses.search( line ) is not None:
        stat = "session"
    else: stat = ""
    
    # for a talk
    if stat == "talk":
        
        # get talk id
        talkid = "".join( line.split(" ")[:2] )[:6]
        
        # get speaker name from next line
        fullname = lines[i+1].split( ";" )[0].strip()
        speaker = fullname.split()[0]
        if fullname == "W. P. Maksym": speaker = "Peter"
        if fullname == "G. B. Berriman": speaker = "Bruce"
        if fullname == "J. Pocahontas Olson": speaker = "Pocohontas"
        if fullname == "S. Thomas Megeath": speaker = "Thomas"
        if fullname == "D. Anish Roshi": speaker = "Anish"
        if fullname == "N. J. Kasdin": speaker = "Jeremy"
        if fullname == "H. P. Stahl": speaker = "Philip"
        if fullname == "A. Smirnov": speaker = "Alexander"
        if fullname == "S. Likhachev": speaker = "Sergey"
        if fullname == "B. S. Gaudi": speaker = "Scott"
        if fullname == "K.E. S. Ford": speaker = "Saavik"
        if fullname == "J. T. Armstrong": speaker = "John"
        if fullname == "G. F. Benedict": speaker = "George"
        if fullname == "Hyunsung David Jun": speaker = "David"
        if fullname == "W. N. Brandt": speaker = "Niel"
        if fullname == "Myungkook J. Jee": speaker = "James"
        speaker_gender = get_gender( speaker )
        
        # print when gender unknown
        if speaker_gender == "x": print talkid, fullname
        
        if withdrawn:
            # print talkid, "withdrawn"
            withdrawn = False
            nw += 1
        
        # record talk info
        talk[tcount].id = talkid
        talk[tcount].speaker = speaker_gender
        tcount += 1
    
    # for a session
    if stat == "session":
        
        # get session id
        sessid = line[:3]
        
        # get chair name from next line
        chair = lines[i+1].split( ":" )[1].split( "(" )[0].strip().split()[0]
        chair_gender = get_gender( chair )
        
        # print when gender unknown
        if chair_gender == "x": print sessid, chair
        
        # record session info
        sess[scount].id = sessid
        sess[scount].chair = chair_gender
        scount += 1

# close the schedule file
f.close()

# cut out all null entries
sess = sess[ where( sess.id ) ]
talk = talk[ where( talk.id ) ]

# write info to files
ascii.write( sess, output="data/sessions.dat" )
ascii.write( talk, output="data/talks.dat" )
