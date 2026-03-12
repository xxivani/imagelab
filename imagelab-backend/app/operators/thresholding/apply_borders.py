import cv2
import numpy as np

from app.operators.base import BaseOperator

_BORDER_TYPE_MAP: dict[str, int] = {
    "CONSTANT": cv2.BORDER_CONSTANT,
    "REFLECT": cv2.BORDER_REFLECT,
    "REPLICATE": cv2.BORDER_REPLICATE,
    "WRAP": cv2.BORDER_WRAP,
}


class ApplyBorders(BaseOperator):
    def compute(self, image: np.ndarray) -> np.ndarray:
        border_all = self.params.get("border_all_sides")
        if border_all is not None:
            top = bottom = left = right = max(0, int(border_all))
        else:
            top = max(0, int(self.params.get("borderTop", 0)))
            bottom = max(0, int(self.params.get("borderBottom", 0)))
            left = max(0, int(self.params.get("borderLeft", 0)))
            right = max(0, int(self.params.get("borderRight", 0)))

        border_type_str = str(self.params.get("border_type", "CONSTANT")).upper()
        if border_type_str not in _BORDER_TYPE_MAP:
            raise ValueError(f"Unknown border type '{border_type_str}'. Valid options: {list(_BORDER_TYPE_MAP.keys())}")
        border_type = _BORDER_TYPE_MAP[border_type_str]

        return cv2.copyMakeBorder(image, top, bottom, left, right, border_type, value=[0, 0, 0])
