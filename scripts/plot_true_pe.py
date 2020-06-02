from ctapipe.visualization import CameraDisplay
from ctapipe.io import SimTelEventSource
from eventio import SimTelFile
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from ctapipe.visualization import mpl_camera

mpl_camera.PIXEL_EPSILON = 0


color = 'afmhot'
path = 'build/simtel-output.zst'

# just to directly get the cam geom
subarray = SimTelEventSource(input_url=path).subarray
geom = subarray.tel[1].camera.geometry

d = CameraDisplay(geom)
d.axes.figure.show()
d.add_colorbar()


for i, e in enumerate(SimTelFile(path).iter_mc_events()):

    true_pe = e['photoelectrons'].get(0)

    if true_pe is not None:
        mc_shower = e['mc_shower']
        energy = mc_shower['energy']
        event_id = e['event_id']
        pe = true_pe['photoelectrons']
        max_pe = int(np.max(pe))

        d.axes.set_title(f'{event_id}: {energy:.2f} TeV')
        d.image = pe
        d.cmap = cm.get_cmap(color, max_pe + 1)

        if max_pe >= 100 and max_pe < 1000:
            plt.savefig(f"build/true_pe_{max_pe:03d}.png", dpi=500)

plt.savefig("build/true_pe.png", dpi=500)
