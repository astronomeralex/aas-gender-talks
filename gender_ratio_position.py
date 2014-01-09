

import numpy as np
import matplotlib.pyplot as plt
import astropy
import astropy.io.ascii as ascii
import collections
import scipy
import scipy.misc
from scipy import stats

def count_mf_questions(data_in):
  N_m = 0
  N_f = 0
  
  for i in np.arange(0, len(data_in)):
    N_m = N_m + data_in['questions'][i].count('M')
    N_f = N_f + data_in['questions'][i].count('F')
  
  return (N_f, N_m)



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

l_f = [len(q) for q in data[f_talks]['questions']]
l_m = [len(q) for q in data[m_talks]['questions']]

plt.clf()
plt.hist(l_m, alpha=0.5)
plt.hist(l_f, alpha=0.5, color='r')
plt.legend(['male speaker', 'female speaker'])
plt.title('Questions asked per talk')
plt.savefig('questions_asked_per_talk.pdf')


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
#print pos_numbers

# binomial errors:
def get_errors_on_ratio(pos_numbers):
  for i in np.arange(0, len(pos_numbers)):
    p_f_est = pos_numbers[i,0] / (pos_numbers[i,0] + pos_numbers[i,1])
    z = 1 - 0.5*0.68
    pos_numbers[i, 3] = pos_numbers[i, 2] - z*np.sqrt(1./(pos_numbers[i,0] + pos_numbers[i,1]) * p_f_est * (1 - p_f_est))
    pos_numbers[i, 4] = pos_numbers[i, 2] + z*np.sqrt(1./(pos_numbers[i,0] + pos_numbers[i,1]) * p_f_est * (1 - p_f_est))
  
  return pos_numbers


get_errors_on_ratio(pos_numbers)

# I did a booboo somewhere and the last line of pos_numbers is empty. Delete it.
pos_numbers = pos_numbers[0:-1]

# get binomial errors where approximation does not work (i.e. where p approaches 0 or 1)
# yes, quick and ugly.
i=7 # the one with zero women in that bin
N = pos_numbers[i,0] + pos_numbers[i,1]
k = pos_numbers[i,0]
p_est = pos_numbers[i,0]/(pos_numbers[i,0] + pos_numbers[i,1])
p_est = np.arange(0.01,0.99, 0.01)
likelihood = scipy.misc.comb(N, k) * p_est**k * (1-p_est)**(N-k)
maxi = np.max(np.log(likelihood))
i_near = np.where(np.abs(np.log(likelihood) - maxi) < 1.)[0]
high = np.max(p_est[i_near])
pos_numbers[i, 3] = 0.
pos_numbers[i, 4] = high

others = np.array([0,1,2,3,4,5,6,8]) # the rest of the bins
for i in others:
  N = pos_numbers[i,0] + pos_numbers[i,1]
  k = pos_numbers[i,0]
  p_est = pos_numbers[i,0]/(pos_numbers[i,0] + pos_numbers[i,1])
  p_est = np.arange(0.01,0.99, 0.01)
  likelihood = scipy.misc.comb(N, k) * p_est**k * (1-p_est)**(N-k)
  maxi = np.max(np.log(likelihood))
  i_near = np.where(np.abs(np.log(likelihood) - maxi) < 0.5)[0]
  low = np.min(p_est[i_near])
  high = np.max(p_est[i_near])
  pos_numbers[i, 3] = low
  pos_numbers[i, 4] = high


np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print pos_numbers

plt.clf()
plt.errorbar(np.arange(1, N_max), pos_numbers.transpose()[2], yerr=(pos_numbers.transpose()[2]-pos_numbers.transpose()[3], pos_numbers.transpose()[4]-pos_numbers.transpose()[2]), lw=2 )
plt.xlabel('Position in queue of questions', fontsize=14)
plt.ylabel('Gender ratio f/(m+f)', fontsize=14)
plt.axis([0, 11, -0.25, 1])
plt.savefig('gender_ratio_by_position_in_question_queue.pdf')






