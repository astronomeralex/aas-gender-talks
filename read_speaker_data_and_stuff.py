

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
print len(dupl)
for i in np.arange(0, len(dupl)):
  "talk ", dupl[i]
  print data['questions'][data['talk'] == dupl[i]]

# assume that discrepancies are mostly because people missed some questions, use the data which has the most questions listed

for i in np.arange(0, len(dupl)):
  i_dupl = np.where(data['talk'] == dupl[i])[0]
  questions = data[i_dupl]['questions']
  l = [len(q) for q in questions]
  kickout = np.where(l < np.max(l))[0]
  keep = np.where(l == np.max(l))[0]
  if len(keep) > 1:
    kickout = np.append(kickout, keep[0:-1])
  
  data = np.delete(data, i_dupl[kickout], 0)
  
# check if it worked:

dupl = [x for x, y in collections.Counter(data['talk']).items() if y > 1]
print "Duplicate talks after cleaning: ", dupl


