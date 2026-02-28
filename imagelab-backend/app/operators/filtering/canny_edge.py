import cv2
import numpy as np

from app.operators.base import BaseOperator


class CannyEdge(BaseOperator):
    def compute(self, image: np.ndarray) -> np.ndarray:
        threshold1 = float(self.params.get("threshold1", 100))
        threshold2 = float(self.params.get("threshold2", 200))

        if len(image.shape) == 3:
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(image, threshold1, threshold2)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
