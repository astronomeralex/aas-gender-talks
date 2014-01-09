

import numpy as np
import matplotlib.pyplot as plt
import astropy
import astropy.io.ascii as ascii
import collections
from scipy import stats

def count_mf_questions(data_in):
  N_m = 0
  N_f = 0
  
  for i in np.arange(0, len(data_in)):
    N_m = N_m + data_in['questions'][i].count('M')
    N_f = N_f + data_in['questions'][i].count('F')
  
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

# check duplicates of talks
dupl = [x for x, y in collections.Counter(data['talk']).items() if y > 1]
print "Duplicate talks: ", dupl
for i in np.arange(0, len(dupl)):
  "talk ", dupl[i]
  print data['questions'][data['talk'] == dupl[i]]

# assume that discrepancies are mostly because people missed some questions, use the data which has the most questions listed

for i in np.arange(0, len(dupl)):
  questions = data['questions'][data['talk'] == dupl[i]]


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




# find out at which position in the talk queue women and men typically ask their question

def position_ratios(data):
  discussion_length = [len(data['questions'][i]) for i in np.arange(0, len(data))]
  N_max = np.max(discussion_length)
  pos_numbers = np.zeros([N_max, 5])
  for i in np.arange(0, N_max-1):
    for j in np.arange(0, len(data)):
      if len(data['questions'][j]) >= (i+1):
        pos_numbers[i,0] = pos_numbers[i,0] + (data['questions'][j][i]=='F')
        pos_numbers[i,1] = pos_numbers[i,1] + (data['questions'][j][i]=='M')
      
  for i in np.arange(0, N_max-1):
    pos_numbers[i,2] = pos_numbers[i,0]/(pos_numbers[i,1]+pos_numbers[i,0])
  
  return (pos_numbers, N_max)

print "testing position ratios"
(pos_numbers, N_max) = position_ratios(data)
print pos_numbers

def get_errors_on_ratio(pos_numbers):
  for i in np.arange(0, len(pos_numbers)):
    samp_size = 10000
    if ((pos_numbers[i,0] > 0) & (pos_numbers[i,1] > 0)):
      sf = stats.poisson.rvs(pos_numbers[i,0], size=samp_size)*np.ones(samp_size, float)
      sm = stats.poisson.rvs(pos_numbers[i,1], size=samp_size)*np.ones(samp_size, float)
      out = sf/(sm + sf)
      out.sort()
      low = out[int(0.16*samp_size)]
      high = out[int(0.84*samp_size)]
      pos_numbers[i, 3] = low
      pos_numbers[i, 4] = high
  
  return pos_numbers


get_errors_on_ratio(pos_numbers)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print pos_numbers

plt.clf()
plt.errorbar(np.arange(1, N_max+1), pos_numbers.transpose()[2], yerr=(pos_numbers.transpose()[2]-pos_numbers.transpose()[3], pos_numbers.transpose()[4]-pos_numbers.transpose()[2]), lw=2 )
plt.xlabel('Position in queue of questions', fontsize=14)
plt.ylabel('Gender ratio f/(m+f)', fontsize=14)
plt.axis([0, 11, -0.25, 1])
plt.savefig('gender_ratio_by_position_in_question_queue.pdf')






