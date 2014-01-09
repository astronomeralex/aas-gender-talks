

import numpy as np
import matplotlib.pyplot as plt
import astropy
import astropy.io.ascii as ascii

def count_mf_questions(data_in):
  N_m = 0
  N_f = 0
  
  for i in np.arange(0, len(data_in)):
    N_m = N_m + data['questions'][i].count('M')
    N_f = N_f + data['questions'][i].count('F')
  
  return (N_f, N_m)




data = ascii.read('data.csv')

# print stuff where no gender is reported

for i in np.arange(0, len(data)):
  if any(data.mask[i]):
    print data[i]

# turns out most of those entries are ones where no questions were reported. Throw them out.

index = np.array([])
for i in np.arange(0, len(data)):
  if any(data.mask[i]):
    index = np.append(index, i)

data.remove_rows(index)

# Don't need mask anymore

data = data._data.data

# This is how to access data in this array:
# For example, print the speaker genders:

print data['speaker']

# Plot number of female and male speakers in sample

#plt.plot(np.array([0,1]), np.array([len(data[data['speaker']=='M']), len(data[data['speaker']=='F'])]), 'o')
#plt.axis([-1, 2, 0, 300])

print "Number of reported talks given by men: ", len(data[data['speaker']=='M'])
print "Number of reported talks given by women: ", len(data[data['speaker']=='F'])
print "Talk ratio f/m: ", np.float(len(data[data['speaker']=='F']))/len(data[data['speaker']=='M'])

# count female/male questions:

(N_f, N_m) = count_mf_questions(data)

print "Number of questions asked by men: ", N_m
print "Number of questions asked by women: ", N_f
print "Questions ratio f/m: ", np.float(N_f)/N_m

# questions ratio for talks given by women/men individually
f_talks = data['speaker'] == 'F'
m_talks = data['speaker'] == 'M'

(N_f_tf, N_m_tf) = count_mf_questions(data[f_talks==True])
(N_f_tm, N_m_tm) = count_mf_questions(data[m_talks==True])


print "In Talks given by women:"
print "Number of questions asked by men: ", N_m_tf
print "Number of questions asked by women: ", N_f_tf
print "Questions ratio f/m: ", np.float(N_f_tf)/N_m_tf

print "In Talks given by men:"
print "Number of questions asked by men: ", N_m_tm
print "Number of questions asked by women: ", N_f_tm
print "Questions ratio f/m: ", np.float(N_f_tm)/N_m_tm




# find out at which position in the talk queue wome and men typically ask their question













