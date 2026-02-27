import cv2
import numpy as np

from app.operators.base import BaseOperator


class CannyEdge(BaseOperator):
    """Applies Canny edge detection to an image.

    Color (BGR) images are converted to grayscale before processing.
    BGRA images have the alpha channel removed. Already-grayscale
    (single-channel 2D or shape (H, W, 1)) images are passed directly
    to the detector. The output is always a 3-channel BGR image with
    white edges on a black background, suitable for downstream pipeline
    operators.

    Params:
        threshold1 (float): Lower hysteresis threshold (default: 100).
            Clamped to >= 0. Swapped with threshold2 if greater.
            Practical range for uint8 images is [0, 255].
        threshold2 (float): Upper hysteresis threshold (default: 200).
            Clamped to >= 0. Must be >= threshold1.
            Practical range for uint8 images is [0, 255].

    Note:
        ``apertureSize`` (Sobel kernel size) and ``L2gradient`` are fixed
        at OpenCV defaults (3 and False, respectively) and are not
        currently exposed as parameters.
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
            elif channels == 1:
                image = image[:, :, 0]
            else:
                raise ValueError(f"Unsupported number of channels: {channels}. Expected 1, 3, or 4.")

        # cv2.Canny requires uint8 input
        if image.dtype != np.uint8:
            if np.issubdtype(image.dtype, np.floating) and image.max() <= 1.0:
                image = image * 255.0
            image = np.clip(image, 0, 255).astype(np.uint8)

        edges = cv2.Canny(image, threshold1, threshold2)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
