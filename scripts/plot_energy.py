import numpy as np
from matplotlib import pyplot as plt
from eventio import SimTelFile

input_path = "build/simtel-output.zst"

energies = []

file = SimTelFile(input_path)

for event in file:
    if event["type"] == "data":
        energies.append(event["mc_shower"]["energy"])

log_intensity = np.log10(energies)

fig, ax = plt.subplots()

ax.hist(log_intensity, histtype="step", bins=20, label="sim_telarray")

ax.set_xlabel("log10(energy / TeV)")

ax.legend()

fig.savefig("build/energy.png")
