import click
import pandas as pd
import numpy as np
from scipy.stats import kstest
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt


def get_bins(x0, x1, n_bins=30):
    x = np.append(x0, x1)
    bin_min = np.min(x[np.isfinite(x)])
    bin_max = np.max(x[np.isfinite(x)])
    return np.linspace(bin_min, bin_max, n_bins + 1)


@click.command()
@click.argument('input_path')
@click.argument('output_path')
def main(input_path, output_path):
    df = pd.read_hdf(input_path, 'events').dropna()

    columns = []
    for col in df.columns:
        c = col.replace('_simtel', '').replace('_facttools', '')
        if c not in columns:
            columns.append(c)

    columns = sorted(columns)

    with PdfPages(output_path) as pdf:
        for col in columns:
            x0 = df[f'{col}_simtel'].to_numpy()
            x1 = df[f'{col}_facttools'].to_numpy()

            bins = get_bins(x0, x1)

            pars = dict(bins=bins, histtype='step')

            fig, ax = plt.subplots()

            ax.hist(x0, label='simtel', **pars)
            ax.hist(x1, label='ceres', **pars)

            stat, p_val = kstest(x0, x1, mode='exact')
            ax.set_title(f'ks: {stat:.4f}')
            ax.legend()

            ax.set_xlabel(col)

            plt.close(fig)

            pdf.savefig(fig)


if __name__ == "__main__":
    main()
