import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt

input_path = "build/events.dl1.h5"

impars = pd.read_hdf(input_path, '/dl1/event/telescope/parameters/tel_001')


def setup():
    return plt.subplots(figsize=(8, 5))


def save(pdf, fig):
    fig.tight_layout()
    pdf.savefig(fig)


def get_bins(lower=None, upper=None, n_bins=None):
    if n_bins is None:
        n_bins = upper - lower + 1

    return np.linspace(lower, upper, n_bins)


with PdfPages('build/hillas.pdf') as pdf:

    fig, ax = setup()
    df = impars[['hillas_length', 'hillas_width']].copy().dropna()

    df.plot.hist(ax=ax, histtype='step', bins=18)
    save(pdf, fig)

    fig, ax = setup()
    intensity = impars['hillas_intensity'].dropna().to_numpy()
    if intensity.size > 0:
        ax.hist(np.log10(intensity), histtype='step', bins=18)
    ax.set_xlabel("log10(intensity)")
    save(pdf, fig)

    fig, ax = setup()
    df = impars[['leakage_intensity_width_1', 'leakage_intensity_width_2']]
    bins = get_bins(0, 1, 21)
    ax.hist(df['leakage_intensity_width_1'], histtype='step', bins=bins)
    ax.hist(df['leakage_intensity_width_2'], histtype='step', bins=bins)
    ax.set_xlabel('leakage')
    ax.legend([1, 2])
    save(pdf, fig)

    fig, ax = setup()
    df = impars['concentration_cog'].dropna().to_numpy()
    if df.size > 0:
        ax.hist(df, histtype='step', bins=18)
    ax.set_xlabel("concentration_cog")
    save(pdf, fig)

    fig, ax = setup()
    df = impars['concentration_core'].dropna().to_numpy()
    bins = 18
    if df.size > 0:
        ax.hist(df, bins=bins, histtype='step')
    ax.set_xlabel("concentration_core")
    save(pdf, fig)

    fig, ax = setup()
    df = impars['morphology_num_pixels'].to_numpy()
    bins = get_bins(0, 40)
    ax.hist(df, bins=bins, histtype='step', align='left')
    ax.set_xlabel("morphology_num_pixels")
    save(pdf, fig)

    fig, ax = setup()
    df = impars['morphology_num_islands'].to_numpy()
    bins = get_bins(-1, 12)
    ax.hist(df, bins=bins, histtype='step', align='left')
    ax.set_xlabel("morphology_num_islands")
    save(pdf, fig)





    # fig, ax = setup()
    # ax.hist2d(np.log10(df['hillas_intensity']), df['hillas_length'], bins=18, norm=LogNorm())
    # ax.set_xlabel("log10(intensity)")
    # ax.set_ylabel("length")
    # save(pdf, fig)

    # fig, ax = setup()
    # ax.hist2d(np.log10(df['hillas_intensity']), df['hillas_width'], bins=18, norm=LogNorm())
    # ax.set_xlabel("log10(intensity)")
    # ax.set_ylabel("width")
    # save(pdf, fig)
