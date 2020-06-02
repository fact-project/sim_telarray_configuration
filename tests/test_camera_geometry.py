from ctapipe.io import SimTelEventSource
from ctapipe.instrument import CameraGeometry

from numpy.testing import assert_allclose

events = SimTelEventSource(input_url="build/simtel-output.zst")
camera = events.subarray.tel[1].camera
geom = camera.geometry.__dict__

fact = CameraGeometry.from_name("FACT").__dict__


def test_n_pixels():
    p = "n_pixels"
    assert_allclose(fact[p], geom[p])


def test_camera_name():
    p = "camera_name"
    # assert fact[p] == geom[p]


def test_pix_id():
    p = "pix_id"
    assert_allclose(fact[p], geom[p])


def test_pix_x():
    p = "pix_x"
    assert_allclose(fact[p], geom[p])


def test_pix_y():
    p = "pix_y"
    assert_allclose(fact[p], geom[p])


def test_pix_area():
    p = "pix_area"
    # assert_allclose(fact[p], geom[p])


def test_pix_type():
    p = "pix_type"
    assert fact[p] == geom[p]


def test_pix_rotation():
    p = "pix_rotation"
    assert_allclose(fact[p], geom[p])


def test_cam_rotation():
    p = "cam_rotation"
    assert_allclose(fact[p], geom[p])


def test__neighbors():
    p = "_neighbors"
    assert fact[p] == geom[p]


def test_frame():
    p = "frame"
    assert fact[p] == geom[p]


def test_border_cache():
    p = "border_cache"
    assert fact[p] == geom[p]


if __name__ == "__main__":
    pass
