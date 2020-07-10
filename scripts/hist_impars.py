import click
import pandas as pd
import numpy as np
from scipy.stats import kstest
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
from fact_plots import plot_bias_resolution


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
            sim_col = f'{col}_simtel'
            cer_col = f'{col}_facttools'
            sim = df[sim_col].to_numpy()
            cer = df[cer_col].to_numpy()

            bins = get_bins(sim, cer, n_bins=20)

            pars = dict(bins=bins, histtype='step')

            fig, axes = plt.subplots(figsize=(10, 5), ncols=3)

            ax = axes[0]

            ax.hist(sim, label='simtel', **pars)
            ax.hist(cer, label='ceres', **pars)

            stat, p_val = kstest(sim, cer, mode='exact')
            ax.set_title(f'ks: {stat:.4f}')
            ax.legend()

            ax.set_xlabel(col)

            ax = axes[1]

            *_, im = ax.hist2d(sim, cer, bins=bins, cmin=1)
            fig.colorbar(im, ax=ax)
            ax.set_xlabel('simtel')
            ax.set_ylabel('ceres')

            ax.plot(
                [bins[0], bins[-1]],
                [bins[0], bins[-1]],
                'k--',
                alpha=0.5,
            )

            ax.set_aspect(1)

            ax = axes[2]
            ax.set_xlabel(col)

            ax_bias, ax_resolution = plot_bias_resolution(
                df[[sim_col, cer_col]].copy(),
                bins=bins,
                ax_bias=ax,
                prediction_key=sim_col,
                true_energy_key=cer_col,
            )

            ax_bias.set_ylabel('bias', color='C0')
            ax_resolution.set_ylabel('resolution', color='C1')

            ax.set_xscale('linear')

            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)


if __name__ == "__main__":
    main()
