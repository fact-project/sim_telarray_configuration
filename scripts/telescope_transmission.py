"""Telescope transmission based on master thesis by S. Mueller.

See Table 3.4, p. 33
"""
import numpy as np
import pandas as pd
from astropy.units import Quantity as Q

# c_all = 2e5
# a_open = Q(13.781, 'm2')

table_3_4 = pd.DataFrame(
    {
        'tilt/deg': [0.00, 1.06, 2.12],
        'c_gapd': [121117, 119549, 114776],
        'c_support': [18584, 19574, 23488],  # c_support = c_all - c_gapd - c_shadow
        'c_shadow': [60299, 60877, 61736],
        'a_telescope/m2': [8.345, 8.237, 7.908],
        'a_support/m2': [1.280, 1.349, 1.618],
    }
)

camera_body_diameter = Q(53, 'cm')
camera_depth = Q(0, 'cm')

a_camera = np.pi * (camera_body_diameter / 2) ** 2
a_sup_only = Q(table_3_4['a_support/m2'], 'm2') - a_camera

shadowing = np.mean(a_sup_only / Q(table_3_4['a_telescope/m2'], 'm2'))
transmission = 1 - shadowing

print(f"Transmission: {transmission:.4f}")
