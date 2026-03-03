import cv2
import numpy as np

from app.operators.base import BaseOperator


class CannyEdge(BaseOperator):
    """Applies Canny edge detection to an image.

    Color (BGR/BGRA) images are converted to grayscale before processing.
    The output is always a 3-channel BGR image with white edges on a black
    background, suitable for downstream pipeline operators.

    Params:
        threshold1 (float): Lower hysteresis threshold (default: 100).
            Clamped to >= 0. Swapped with threshold2 if greater.
        threshold2 (float): Upper hysteresis threshold (default: 200).
            Clamped to >= 0. Must be >= threshold1.
    """

    def compute(self, image: np.ndarray) -> np.ndarray:
        threshold1 = max(0.0, float(self.params.get("threshold1", 100)))
        threshold2 = max(0.0, float(self.params.get("threshold2", 200)))

        # Enforce hysteresis ordering
        if threshold1 > threshold2:
            threshold1, threshold2 = threshold2, threshold1

        if len(image.shape) == 3:
            channels = image.shape[2]
            if channels == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            elif channels == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                raise ValueError(f"Unsupported number of channels: {channels}. Expected 3 (BGR) or 4 (BGRA).")

        # cv2.Canny requires uint8 input
        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)

        edges = cv2.Canny(image, threshold1, threshold2)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
