import pandas as pd
from numpy import exp, linspace


def pulse(x):
    return (
        1.239
        * (1 - 1 / (1 + exp((0.5 * x - 2.851) / 1.063)))
        * exp(-(0.5 * x - 2.851) / 19.173)
    )


def main(output_path):
    n_px = 310
    x_min = -10
    x_max = 300
    x = linspace(x_min, x_max, n_px + 1)

    df = pd.DataFrame({'x': x / 2, 'pulse': pulse(x)})

    df.to_csv(output_path, sep='\t', header=False, index=False)


if __name__ == "__main__":
    main("build/pulse_shape.dat")
