import pandas as pd
from tqdm import tqdm

KEY = "/dl1/event/telescope/parameters/tel_001"


def main():
    data = []

    for file in tqdm(snakemake.input):
        data.append(pd.read_hdf(file, KEY))

    df = pd.concat(data)

    df.to_hdf(str(snakemake.output), key='events')


if __name__ == "__main__":
    main()
