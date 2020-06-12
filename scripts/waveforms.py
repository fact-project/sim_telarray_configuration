import numpy as np
from ctapipe.io import SimTelEventSource
from matplotlib import pyplot as plt

n_pixels = 3

p = "build/simtel-output.zst"

s = SimTelEventSource(p)

for event in s:
    energy = event.mc.energy
    break

r0 = event.r0.tel[1]
r1 = event.r1.tel[1]

brightest_pixels = np.sum(r0.waveform[0, :, :], axis=1).argsort()[::-1]

fig, (ax0, ax1) = plt.subplots(nrows=2)

for i_pix in brightest_pixels[:n_pixels]:
    ax0.plot(r0.waveform[0, i_pix, :], "-", label=f"{i_pix}")
    ax1.plot(r1.waveform[i_pix, :], "-", label=f"{i_pix}")

for i, ax in enumerate((ax0, ax1)):
    ax.set_title(f"R{i} Waveform")
    ax.set_xlabel("sample")

    if n_pixels <= 5:
        ax.legend(title="pixel id")

fig.tight_layout()
fig.savefig("build/waveforms.png")
