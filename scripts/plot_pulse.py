import numpy as np
from matplotlib import pyplot as plt

x, y = np.genfromtxt("build/pulse_shape.dat", unpack=True)

fig, ax = plt.subplots()

ax.plot(x, y)
ax.set_xlabel("sample")
ax.set_title("Pulse Shape")

fig.savefig("build/pulse_shape.png")
