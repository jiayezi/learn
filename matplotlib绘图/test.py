import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 20, 0.1)  # start,stop,step
y = np.tan(x)
plt.plot(x, y)
plt.show()

