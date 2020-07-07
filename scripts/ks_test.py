import click
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kstest


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

    stats = []
    p_values = []
    for col in columns:
        s, p = kstest(
            df[f'{col}_simtel'],
            df[f'{col}_facttools'],
            mode='exact',
        )
        stats.append(s)
        p_values.append(p)

    order = np.argsort(columns)
    columns = np.asarray(columns)[order]
    stats = np.asarray(stats)[order]
    p_values = np.asarray(p_values)[order]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_title('KS Test of Image Parameters')

    ax.plot(stats, columns, 'bo', label='statistic')
    ax.set_xlabel('statistic')
    ax.grid(axis='y')
    ax.axvline(x=0, color='b', linewidth=0.5)
    ax = ax.twiny()
    ax.plot(p_values, columns, 'r.', label='p-value')
    ax.set_xlabel('p-value')
    ax.set_xscale('log')
    ax.axvline(x=1, color='r', linewidth=0.5)

    fig.legend(loc='lower left', title='ks test')
    fig.tight_layout()

    fig.savefig(output_path, dpi=120)


if __name__ == "__main__":
    main()
