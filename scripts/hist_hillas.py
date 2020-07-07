import click
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt


def setup():
    return plt.subplots(figsize=(8, 5))


def save(pdf, fig):
    fig.tight_layout()
    pdf.savefig(fig)


def get_bins(n_bins, bin_min=None, bin_max=None, bin_step=None):
    assert n_bins is not None or bin_step is not None

    if n_bins is None:
        n_bins = int((bin_max - bin_min) / bin_step) + 1

    if bin_min is None and bin_max is None and bin_step is None:
        bins = n_bins
    else:
        bins = np.linspace(bin_min, bin_max, n_bins)

    return bins


@click.command()
@click.argument('input_path')
@click.argument('output_path')
def main(input_path, output_path):
    df = pd.read_hdf(input_path, 'events')

    pars = dict(histtype='step')

    with PdfPages(output_path) as pdf:

        fig, ax = setup()
        bins = get_bins(None, 0, 0.05, 0.001)
        ax.hist(
            df['hillas_length_simtel'],
            label='simtel',
            bins=bins,
            **pars
        )
        ax.hist(
            df['hillas_length_facttools'],
            label='ceres',
            bins=bins,
            **pars
        )
        ax.legend()
        ax.set_xlabel('hillas_length')
        save(pdf, fig)

        fig, ax = setup()
        bins = get_bins(51, 0, 0.015)
        ax.hist(
            df['hillas_width_simtel'],
            label='simtel',
            bins=bins,
            **pars
        )
        ax.hist(
            df['hillas_width_facttools'],
            label='ceres',
            bins=bins,
            **pars
        )
        ax.legend()
        ax.set_xlabel('hillas_width')
        save(pdf, fig)

        fig, ax = setup()
        bins = get_bins(None, 1.5, 4.5, 0.1)
        ax.hist(
            np.log10(df['hillas_intensity_simtel']),
            label='simtel',
            bins=bins,
            **pars
        )
        ax.hist(
            np.log10(df['hillas_intensity_facttools']),
            label='ceres',
            bins=bins,
            **pars
        )
        ax.legend()
        ax.set_xlabel('log10(hillas_intensity)')
        save(pdf, fig)

if __name__ == "__main__":
    main()
