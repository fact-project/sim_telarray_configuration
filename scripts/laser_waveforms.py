import numpy as np
from eventio import SimTelFile
from matplotlib import pyplot as plt

n_pixels = 10

p = "build/simtel-output.zst"

s = SimTelFile(p)

for event in s:
    if event['type'] == 'calibration':
        break

adc_samples = event['telescope_events'][1]['adc_samples']
brightest_pixels = np.sum(adc_samples[0, :, :], axis=1).argsort()[::-1]

fig, ax0 = plt.subplots(nrows=1)

for i_pix in brightest_pixels[:n_pixels]:
    ax0.plot(adc_samples[0, i_pix, :], "-", label=f"{i_pix}")

for i, ax in enumerate([ax0]):
    ax.set_title("ADC Samples of Laser (Calibration) Events")
    ax.set_xlabel("sample")

    ax.legend(title="pixel id")

fig.tight_layout()
fig.savefig("build/laser_waveforms.png")
