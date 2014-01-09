

import numpy as np
import matplotlib.pyplot as plt
import astropy
import astropy.io.ascii as ascii


data = ascii.read('Hackday/data.csv')

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

plt.plot(np.array([0,1]), np.array([len(data[data['speaker']=='M']), len(data[data['speaker']=='F'])]), 'o')
plt.axis([-1, 2, 0, 300])








