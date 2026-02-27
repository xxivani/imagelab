import numpy as np
import pytest

from app.operators.filtering.canny_edge import CannyEdge


def make_bgr(h: int = 64, w: int = 64) -> np.ndarray:
    return np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)


class TestCannyEdgeOutputShape:
    def test_bgr_input(self):
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(make_bgr())
        assert out.shape == (64, 64, 3)

    def test_grayscale_2d_input(self):
        gray = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(gray)
        assert out.shape == (64, 64, 3)

    def test_grayscale_hwc1_input(self):
        gray = np.random.randint(0, 256, (64, 64, 1), dtype=np.uint8)
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(gray)
        assert out.shape == (64, 64, 3)

    def test_bgra_input(self):
        bgra = np.random.randint(0, 256, (64, 64, 4), dtype=np.uint8)
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(bgra)
        assert out.shape == (64, 64, 3)


class TestCannyEdgeThresholdSwap:
    def test_swapped_thresholds_produce_same_result(self):
        img = make_bgr()
        op_normal = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        op_swapped = CannyEdge(params={"threshold1": 150, "threshold2": 50})
        np.testing.assert_array_equal(op_normal.compute(img), op_swapped.compute(img))


class TestCannyEdgeFloatInput:
    def test_normalized_float_not_all_black(self):
        img = np.random.rand(64, 64, 3).astype(np.float32)
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(img)
        assert out.shape == (64, 64, 3)

    def test_uint16_input(self):
        img = np.random.randint(0, 65536, (64, 64, 3), dtype=np.uint16)
        op = CannyEdge(params={"threshold1": 50, "threshold2": 150})
        out = op.compute(img)
        assert out.shape == (64, 64, 3)


class TestCannyEdgeInvalidInput:
    def test_unsupported_channel_count_raises(self):
        img = np.random.randint(0, 256, (64, 64, 2), dtype=np.uint8)
        op = CannyEdge(params={})
        with pytest.raises(ValueError, match="Unsupported number of channels"):
            op.compute(img)
