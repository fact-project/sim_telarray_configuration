import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def main():
    data = pd.read_hdf(str(snakemake.input), 'events')

    print(f"{len(data.dropna())} Events.")

    intensity_simtel = data['hillas_intensity_simtel'].values
    intensity_ceres = data['hillas_intensity_facttools'].values

    fig, ax = plt.subplots()

    bin_max = 5
    bin_min = 1
    bin_step = 0.1
    n_bins = int((bin_max - bin_min) / bin_step)
    bins = np.linspace(bin_min, bin_max, n_bins + 1)

    ax.hist(
        np.log10(intensity_simtel),
        bins=bins,
        label=f'simtel: {np.isfinite(intensity_simtel).sum()}',
        histtype='step',
    )
    ax.hist(
        np.log10(intensity_ceres),
        bins=bins,
        label=f'ceres: {np.isfinite(intensity_ceres).sum()}',
        histtype='step',
    )
    ax.set_xlabel('log10(intensity)')
    ax.set_ylabel('# events')
    ax.legend(title=f'Events ({len(data.dropna())})')

    fig.savefig(str(snakemake.output))


if __name__ == "__main__":
    main()
