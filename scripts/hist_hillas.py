import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt

input_path = "build/events.dl1.h5"

impars = pd.read_hdf(input_path, '/dl1/event/telescope/parameters/tel_001')

cols = ['hillas_length', 'hillas_width', 'hillas_intensity']

df = impars[cols].dropna()


def setup():
    return plt.subplots(figsize=(8, 5))


def save(pdf, fig):
    fig.tight_layout()
    pdf.savefig(fig)


with PdfPages('build/hillas.pdf') as pdf:

    fig, ax = setup()
    df[['hillas_length', 'hillas_width']].plot.hist(ax=ax, histtype='step', range=[0, 0.05], bins=50)
    save(pdf, fig)

    fig, ax = setup()
    ax.hist(np.log10(df['hillas_intensity']), histtype='step', bins=50)
    ax.set_xlabel("log10(intensity)")
    save(pdf, fig)

    fig, ax = setup()
    ax.hist2d(np.log10(df['hillas_intensity']), df['hillas_length'], bins=50, norm=LogNorm())
    ax.set_xlabel("log10(intensity)")
    ax.set_ylabel("length")
    save(pdf, fig)

    fig, ax = setup()
    ax.hist2d(np.log10(df['hillas_intensity']), df['hillas_width'], bins=50, norm=LogNorm())
    ax.set_xlabel("log10(intensity)")
    ax.set_ylabel("width")
    save(pdf, fig)
