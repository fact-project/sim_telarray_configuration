"""Convert Ceres Mirror Configuration To Sim_TelArray Format.

Needs `examples/Ceres_12/reflector.txt` from github.com/fact-project/mopro3.
"""
import numpy as np
import pandas as pd


def main():
    ceres = pd.read_csv(
        "config/reflector.txt",
        sep=r"\s+",
        nrows=30,
        header=None,
        names=["x", "y", "z", "nx", "ny", "nz", "F", "Type", "fD"],
    )

    simtel = pd.DataFrame(
        columns=[
            "x_pos",
            "y_pos",
            "diameter",
            "focal_length",
            "shape_code",
            "separator",
            "z_pos",
            "mirror_number_unused",
            "n_x_unused",
            "n_y_unused",
            "n_z_unused",
            "dist_to_optical_axis_unused",
        ]
    )

    simtel["separator"] = "#%"
    simtel["mirror_number_unused"] = ceres.index
    simtel["x_pos"] = ceres["x"]
    simtel["y_pos"] = ceres["y"]
    simtel["z_pos"] = ceres["z"]
    simtel["n_x_unused"] = ceres["nx"]
    simtel["n_y_unused"] = ceres["ny"]
    simtel["n_z_unused"] = ceres["nz"]
    simtel["shape_code"] = np.where(ceres["Type"] == "Hex", 3, pd.NA)  # Hex?
    simtel["focal_length"] = ceres["F"]
    simtel["diameter"] = ceres["fD"]

    simtel.to_csv("build/mirror_FACT.dat", sep="\t", header=False, index=False)


if __name__ == "__main__":
    main()
