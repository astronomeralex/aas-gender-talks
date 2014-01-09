
# get binomial errors where approximation does not work (i.e. where p approaches 0 or 1)
i=7
N = pos_numbers[i,0] + pos_numbers[i,1]
k = pos_numbers[i,0]
p_est = pos_numbers[i,0]/(pos_numbers[i,0] + pos_numbers[i,1])
p_est = np.arange(0.01,0.99, 0.01)
likelihood = scipy.misc.comb(N, k) * p_est**k * (1-p_est)**(N-k)
print np.log(likelihood)


