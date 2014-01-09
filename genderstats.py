#run using ipython
#assumes you've already ran read_speaker_data_and_stuff.py
# run using execfile("genderstats.py")

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

print "First Question --"
print "Men:", mfirstq, "(%.1f"%(float(mfirstq)/numtalks*100) + "%)"
print "Women:", ffirstq, "(%.1f"%(float(ffirstq)/numtalks*100) + "%)"
