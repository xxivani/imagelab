import cv2
import numpy as np

from app.operators.base import BaseOperator


class GaussianNoise(BaseOperator):
    def compute(self, image: np.ndarray) -> np.ndarray:
        mean = float(self.params.get("mean", 0))
        sigma = float(self.params.get("sigma", 25))
        sigma = max(1.0, sigma)

        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        noise = np.random.normal(mean, sigma, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)
