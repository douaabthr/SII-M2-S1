import numpy as np
R=2
N=6
wt=0.342423
ri=2
ni=5
numerator = (ri + 0.5) / (R - ri + 0.5)
denominator =  (ni - ri + 0.5)/(N - ni - R + ri + 0.5)
if denominator > 0 and numerator > 0:
    idf_prob = np.log10(numerator / denominator)
else:
    idf_prob = 0.0
print(wt* idf_prob)