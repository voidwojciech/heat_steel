import numpy as np
import matplotlib.pyplot as plt



c = [0,1,2,3,4,5,5,5,6,6]
c = [0,1,2,3,4,5,5,5,6,10]
c = [0,1,2,3,4,5.1,5.1,5.1,6,10]

h = plt.hist(c, bins=10)
plt.show()