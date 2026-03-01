import cv2
import numpy as np

from app.operators.base import BaseOperator


class SaltPepperNoise(BaseOperator):
    def compute(self, image: np.ndarray) -> np.ndarray:
        density = float(self.params.get("density", 0.05))
        density = max(0.0, min(1.0, density))

        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        result = image.copy()
        total_pixels = image.shape[0] * image.shape[1]
        num_affected = int(total_pixels * density)

        # Add salt (white pixels)
        salt_coords = (
            np.random.randint(0, image.shape[0], num_affected // 2),
            np.random.randint(0, image.shape[1], num_affected // 2),
        )
        result[salt_coords] = 255

        # Add pepper (black pixels)
        pepper_coords = (
            np.random.randint(0, image.shape[0], num_affected // 2),
            np.random.randint(0, image.shape[1], num_affected // 2),
        )
        result[pepper_coords] = 0

        return result
