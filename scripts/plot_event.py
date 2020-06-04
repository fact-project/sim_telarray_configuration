import numpy as np
from matplotlib import colors, cm, pyplot as plt
from eventio import SimTelFile
from ctapipe.io import SimTelEventSource
from ctapipe.visualization import CameraDisplay

bad_pixels = {'color': 'black', 'alpha': 0.1}
cw = cm.coolwarm
cw.set_bad(**bad_pixels)
vi = cm.viridis
vi.set_bad(**bad_pixels)

p = "build/simtel-output.zst"
f = SimTelFile(p)
s = SimTelEventSource(p)

geom = s.subarray.tel[1].camera.geometry

fig, (ax_im, ax_t) = plt.subplots(ncols=2, figsize=(8, 4))

disp_im = CameraDisplay(geom, ax=ax_im, cmap=vi)
disp_im.add_colorbar()
disp_t = CameraDisplay(geom, ax=ax_t, cmap=cw)
disp_t.add_colorbar()

fig.tight_layout()
fig.show()


def plot(pe):
    image = pe['photoelectrons']
    image[image == 0] = np.nan

    time = np.empty_like(image)
    mask = pe['pixel_id']
    time[:] = np.nan
    time[mask] = pe['time'] - np.mean(pe['time'])

    disp_im.image = image
    disp_t.image = time


for event in f.iter_mc_events():
    if event['photoelectrons'] != {}:
        pe = event['photoelectrons'][0]

        if np.sum(pe['photoelectrons']) > 100:
            plot(pe)
            plt.pause(0.2)
