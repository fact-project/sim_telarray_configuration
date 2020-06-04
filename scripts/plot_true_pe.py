from ctapipe.visualization import CameraDisplay
from ctapipe.io import SimTelEventSource
from eventio import SimTelFile
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from ctapipe.visualization import mpl_camera

mpl_camera.PIXEL_EPSILON = 0


path = 'build/simtel-output.zst'

# just to directly get the cam geom
subarray = SimTelEventSource(input_url=path).subarray
geom = subarray.tel[1].camera.geometry

fig, ax = plt.subplots()

im_disp = CameraDisplay(geom, ax=ax)
fig.show()
im_disp.add_colorbar()


for e in SimTelFile(path).iter_mc_events():

    true_pe = e['photoelectrons'].get(0)

    if true_pe is not None:
        mc_shower = e['mc_shower']
        energy = mc_shower['energy']
        event_id = e['event_id']
        pe = true_pe['photoelectrons']
        time = np.empty(1440)
        time[true_pe['pixel_id']] = true_pe['time']
        max_pe = int(np.max(pe))

        im_disp.axes.set_title(f'{event_id}: {energy:.2f} TeV')
        im_disp.image = pe

        if max_pe >= 100 and max_pe < 1000:
            plt.savefig(f"build/true_pe_{max_pe:03d}.png", dpi=500)

plt.savefig("build/true_pe.png", dpi=500)
