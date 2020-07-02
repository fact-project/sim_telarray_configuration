import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def main():
    data = pd.read_hdf(str(snakemake.input), 'events')

    print(f"{len(data.dropna())} Events.")

    intensity_simtel = data['hillas_intensity_simtel'].values
    intensity_ceres = data['hillas_intensity_facttools'].values

    fig, ax = plt.subplots()

    ax.set_title('log10(intensity)')
    ax.set_xlabel('sim_telarray')
    ax.set_ylabel('ceres')
    ax.set_aspect(1)

    bin_max = 5
    bin_min = 1
    bin_step = 0.2
    n_bins = int((bin_max - bin_min) / bin_step)
    bins = np.linspace(bin_min, bin_max, n_bins + 1)

    *_, im = ax.hist2d(
        np.log10(intensity_simtel),
        np.log10(intensity_ceres),
        bins=bins,
        cmin=1,
    )
    fig.colorbar(im, ax=ax, label='# events')

    ax.plot([bin_min, bin_max], [bin_min, bin_max], 'k--', alpha=0.5)

    fig.savefig(str(snakemake.output))


if __name__ == "__main__":
    main()
