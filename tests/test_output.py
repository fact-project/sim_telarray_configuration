from eventio import SimTelFile
import numpy as np

input_path = "build/simtel-output.zst"

f = SimTelFile(input_path)

tel = f.telescope_descriptions[1]
cam = tel['camera_settings']


def test_focal_length():
    assert np.isclose(cam['focal_length'], [4.889], atol=0.01)


def test_n_pixels():
    assert cam['n_pixels'] == 1440
