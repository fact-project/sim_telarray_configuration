import pandas as pd

KEY = "events"
INDEX = ["obs_id", "event_id"]


def main():
    df_facttools = pd.read_hdf(snakemake.input["fact_tools"], KEY).set_index(INDEX)
    df_simtel = pd.read_hdf(snakemake.input["simtel"], KEY)
    df_simtel["event_id"] /= 1000
    df_simtel.set_index(INDEX, inplace=True)

    df = df_facttools.join(df_simtel, lsuffix="_facttools", rsuffix="_simtel")

    df.to_hdf(str(snakemake.output), KEY)


if __name__ == "__main__":
    main()
