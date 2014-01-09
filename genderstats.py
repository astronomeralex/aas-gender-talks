#run using ipython
#assumes you've already ran read_speaker_data_and_stuff.py
# run using execfile("genderstats.py")

import re

numtalks = len(data)
mtalks = len(data[data["speaker"] == "M"])
ftalks = len(data[data["speaker"] == "F"])

print "Total Number of Talks Recorded:", numtalks
print "Talks Given by Men:", mtalks, "(%.1f"%(float(mtalks)/numtalks*100) + "%)"
print "Talks Given by Women:", ftalks, "(%.1f"%(float(ftalks)/numtalks*100) + "%)"
print

qstring = ''
for i in data["questions"]:
    qstring = qstring + i

numqs = len(qstring)
mqs = qstring.count("M")
fqs = qstring.count("F")

print "Total Questions: ", numqs
print "Questions by Males:", mqs, "(%.1f"%(float(mqs)/numqs*100) + "%)"
print "Questions by Females:", fqs, "(%.1f"%(float(fqs)/numqs*100) + "%)"
print

#first question
mfirstq = 0
ffirstq = 0
for i in data["questions"]:
    if i[0] == "M":
        mfirstq += 1
    else:
        ffirstq += 1

mfraction = float(mfirstq)/numtalks
ffraction = float(ffirstq)/numtalks

print "First Question:"
print "Men:", mfirstq, "(%.1f"%(mfraction*100) + "%)"
print "Women:", ffirstq, "(%.1f"%(ffraction*100) + "%)"
print 

#two point function time
tpmm = 0
tpmf = 0
tpfm = 0
tpff = 0
for i in data["questions"]:
    tpmm += len(re.findall('(?=MM)', i))
    tpmf += len(re.findall('(?=MF)', i))
    tpfm += len(re.findall('(?=FM)', i))
    tpff += len(re.findall('(?=FF)', i))

tptotal = tpmm + tpmf + tpfm + tpff

print "Two-Gram Total:", tptotal
print "Two-Gram MM:", tpmm, "(%.1f"%(float(tpmm)/tptotal*100) + "%);", "Expected:", int(round(tptotal*mfraction**2))
print "Two-Gram MF:", tpmf, "(%.1f"%(float(tpmf)/tptotal*100) + "%);", "Expected:", int(round(tptotal*mfraction*ffraction))
print "Two-Gram FM:", tpfm, "(%.1f"%(float(tpfm)/tptotal*100) + "%);", "Expected:", int(round(tptotal*mfraction*ffraction))
print "Two-Gram FF:", tpff, "(%.1f"%(float(tpff)/tptotal*100) + "%);", "Expected:", int(round(tptotal*ffraction**2))
print

#three-gram time
tgmmm = 0
tgmmf = 0
tgmfm = 0
tgfmm = 0
tgmff = 0
tgfmf = 0
tgffm = 0
tgfff = 0

for i in data["questions"]:
    tgmmm += len(re.findall('(?=MMM)', i))
    tgmmf += len(re.findall('(?=MMF)', i))
    tgmfm += len(re.findall('(?=MFM)', i))
    tgfmm += len(re.findall('(?=FMM)', i))
    tgmff += len(re.findall('(?=MFF)', i))
    tgfmf += len(re.findall('(?=FMF)', i))
    tgffm += len(re.findall('(?=FFM)', i))
    tgfff += len(re.findall('(?=FFF)', i))

tgtotal = tgmmm + tgmmf + tgmfm + tgfmm + tgmff + tgfmf + tgffm + tgfff
print "Three-Gram Total:", tgtotal
print "Three-Gram MMM:", tgmmm, "(%.1f"%(float(tgmmm)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction**3))
print "Three-Gram MMF:", tgmmf, "(%.1f"%(float(tgmmf)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction**2 * ffraction))
print "Three-Gram MFM:", tgmfm, "(%.1f"%(float(tgmfm)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction**2 * ffraction))
print "Three-Gram FMM:", tgfmm, "(%.1f"%(float(tgfmm)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction**2 * ffraction))
print "Three-Gram MFF:", tgmff, "(%.1f"%(float(tgmff)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction* ffraction**2))
print "Three-Gram FMF:", tgfmf, "(%.1f"%(float(tgfmf)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction* ffraction**2))
print "Three-Gram FFM:", tgffm, "(%.1f"%(float(tgffm)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*mfraction* ffraction**2))
print "Three-Gram FFF:", tgfff, "(%.1f"%(float(tgfff)/tgtotal*100) + "%);", "Expected:", int(round(tgtotal*ffraction**3))
print

#talks with only one question
singleq = ''
sqnum = 0
for i in data["questions"]:
    if len(i) == 1:
        singleq = singleq + i
        sqnum += 1
        
msq = singleq.count("M")
msqfrac = float(msq) / sqnum
fsq = singleq.count("F")
fsqfrac = float(fsq) / sqnum
print "Talks with Only One Question:", sqnum
print "Male:", msq, "(%.1f"%(msqfrac*100) + "%)"
print "Female:", fsq, "(%.1f"%(fsqfrac*100) + "%)"
print


