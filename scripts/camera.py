import pandas as pd
from ctapipe.instrument import CameraGeometry
from fact.instrument import get_pixel_dataframe
from astropy import units as u
from astropy.units import Quantity as Q

output_path = "build/camera_FACT.dat"


def main():
    geom = CameraGeometry.from_name("FACT")

    df = pd.DataFrame(
        {"pix_id": geom.pix_id, "pix_x": geom.pix_x, "pix_y": geom.pix_y},
    ).set_index("pix_id")

    cols = ["CHID", "trigger_patch_id"]
    fact_pixels = get_pixel_dataframe()
    fact_pixels = fact_pixels[cols].set_index("CHID")

    sim_tel_camera = df.join(fact_pixels)

    general_cmt = """
# FACT Camera

# File generated with `config.py`
"""

    pixtype_cmt = """
# PixType format:
# Par.  1: pixel type (here always 1)
#       2: PMT type (must be 0)
#       3: cathode shape type (see below)
#       4: visible cathode diameter [cm]
#       5: funnel shape type (see below)
#       6: funnel diameter (flat-to-flat for hexagons and squares) [cm]
#       7: depth of funnel [cm]
#       8: a) funnel efficiency "filename",   b) funnel plate transparency
#       9: a) optional wavelength "filename", b) funnel wall reflectivity
# Cases a) and b) are distinguished by the format of parameter 8: a quoted
# string indicates case a) while a real number indicates case b).
# In case a) in column 8, columns 3, 4, and 7 are not used. If in case a)
# the optional file name for the wavelength dependence is provided, the
# overall scale in the file provided as parameter 8 is ignored because
# it is rescaled such that the average over all mirrors is equal to
# the given wavelength dependent value.
#
# Shape types: 0: circ., 1: hex(flat x), 2: sq., 3: hex(flat y)
"""

    shape = {
        "circ": 0,
        "hex(flat x)": 1,
        "sq": 2,
        "hex(flat y)": 3,
    }

    pixtype = {
        1: 1,  # pixel type (here always 1)
        2: 0,  # PMT type (must be 0)
        3: shape["sq"],  # cathode shape type (see below)
        4: Q(2.8, u.mm).to_value(u.cm),  # visible cathode diameter [cm]
        5: shape["hex(flat y)"],  # funnel shape type (see below)
        6: Q(9.5, u.mm).to_value(u.cm),  # funnel diameter (flat-to-flat for hex.) [cm]
        7: Q(20, u.mm).to_value(u.cm),  # depth of funnel [cm]
        # double quotes needed!
        8: '"cone-angular-acceptance.txt"',  # a) funnel efficiency "filename",   b) funnel plate transparency
        # 9: 1, # '"cone-angular-acceptance.txt"',  # a) optional wavelength "filename", b) funnel wall reflectivity
    }

    # pixtype_str = 'PixType {} {} {} {} {} {} {} {} {}'.format(*pixtype.values())
    pixtype_str = "PixType"
    for val in pixtype.values():
        pixtype_str += f" {val}"

    pixel_cmt = """
# Pixel format:
# Par.  1: pixel number (starting at 0)
#       2: x position [cm]
#       3: y position [cm]
#       4: drawer/module number
#       5: board number in module
#       5: channel number n board
#       6: board Id number ('0x....')
#       7: pixel on (is on if parameter is missing)
"""

    pixel = pd.DataFrame(
        {
            "keyword": "Pixel",
            "pix_num": sim_tel_camera.index,
            "pix_type": 1,  # set pixel type above
            "x_pos": Q(sim_tel_camera["pix_x"], u.m).to_value(u.cm),
            "y_pos": Q(sim_tel_camera["pix_y"], u.m).to_value(u.cm),
            "module_number": sim_tel_camera["trigger_patch_id"],
            "board_number_in_module": sim_tel_camera["trigger_patch_id"],  # sowas wie patch_id?
            "channel_number_in_board": 0,
            "board_id_number": sim_tel_camera["trigger_patch_id"],
            "pixel_on": 1,  # dead pixels?
        }
    )

    trigger_cmt = """
# AnalogSumTrigger using all pixels from a single trigger patch:
"""

    trigger_str = ""
    trigger_str_prefix = "Trigger * of "
    for idx, grp in sim_tel_camera.groupby('trigger_patch_id'):
        trigger_str += trigger_str_prefix
        trigger_str += " ".join(map(str, list(grp.index))) + "\n"

    with open(output_path, "w") as f:
        f.write(general_cmt + "\n")
        f.write(pixtype_cmt + "\n")
        f.write(pixtype_str + "\n")
        f.write(pixel_cmt + "\n")

    pixel.to_csv(output_path, sep="\t", header=False, index=False, mode="a")

    with open(output_path, "a") as f:
        f.write(trigger_cmt + "\n")
        f.write(trigger_str + "\n")


if __name__ == "__main__":
    main()
