import pathlib
from typing import Union, IO, Tuple, List, Optional
import svgpathtools
import io
import base64
import numpy as np
from numpy.typing import NDArray

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class SVGPixelator:
    file: IO
    aspect_ratio: Tuple[int, int]
    pixelation_level: int

    _max_ratio = (100, 100)
    _min_ratio = (1, 1)
    _invalid_ratio_msg = 'Invalid ratio format!'

    class InvalidRatioFormat(ValueError):
        pass

    def __init__(self, file: IO, aspect_ratio: Union[str, None], pixelation_level: int) -> None:
        self.file = file
        self.aspect_ratio = self.parse_aspect_ratio(aspect_ratio)
        self.pixelation_level = pixelation_level

    # def validate_pixelation_level(self, _pixelation_level: int) -> bool:
    #     return 1 <= _pixelation_level <= 100

    def is_aspect_ratio_valid(self, _ratios: List[str]) -> Tuple[bool, Optional[str]]:
        if len(_ratios) != 2:
            msg = 'Invalid ratio format!'
            return False, msg

        if not all(map(lambda x: x.isdigit(), _ratios)):
            msg = 'All values should be numbers!'
            return False, msg

        if not self._min_ratio[0] <= int(_ratios[0]) <= self._max_ratio[0]:
            msg = 'First or both numbers are out of range! (1-100)'
            return False, msg
        if not self._min_ratio[1] <= int(_ratios[1]) <= self._max_ratio[1]:
            msg = 'Second number is out of range! (1-100)'
            return False, msg

        return True, None

    def parse_aspect_ratio(self, _aspect_ratio: str) -> Tuple[int, int]:
        if not ':' in _aspect_ratio and not '/' in _aspect_ratio:
            raise self.InvalidRatioFormat(self._invalid_ratio_msg)

        ratios = []
        if ':' in _aspect_ratio:
            ratios = _aspect_ratio.split(':')
        elif '/' in _aspect_ratio:
            ratios = _aspect_ratio.split('/')

        is_valid, error_msg = self.is_aspect_ratio_valid(ratios)
        if is_valid:
            return int(ratios[0]), int(ratios[1])
        else:
            raise self.InvalidRatioFormat(error_msg)



    def extract_all_paths(self, num_samples=1000) -> NDArray[np.float64]:
        """Extracts all path elements and converts them to a single NumPy array of points."""
        paths, _ = svgpathtools.svg2paths(self.file)

        all_points = []
        for path in paths:
            for segment in path:
                for t in np.linspace(0, 1, num_samples):
                    point = segment.point(t)
                    all_points.append((point.real, point.imag))

        return np.array(all_points)

    @staticmethod
    def snap_to_grid(points: NDArray[np.float64], pixel_size: Union[int, float] = 10) -> NDArray[np.float64]:
        """Snap a set of points to a pixel grid."""
        snapped = np.unique(np.round(points / pixel_size) * pixel_size, axis=0)
        snapped[:, 1] *= -1  # Flip Y-axis
        return snapped

    @staticmethod
    def clean_plot() -> None:
        plt.axis("off")
        plt.gca().set_xticks([])
        plt.gca().set_yticks([])
        plt.gca().set_frame_on(False)

    def build_and_save_plot(self, _original_points: NDArray[np.float64],
                            _pixelated_points: NDArray[np.float64], _save_to: Union[pathlib.Path, str, io.BytesIO]) -> None:
        """Plot original and pixelated points for visualization."""
        plt.figure(figsize=self.aspect_ratio)
        self.clean_plot()

        plt.scatter(_pixelated_points[:, 0], -_pixelated_points[:, 1], s=10, c='black')
        plt.savefig(_save_to, format="png", bbox_inches="tight", pad_inches=0)
        plt.close()

    def get_final_image_base64(self) -> str:
        original_points = self.extract_all_paths(num_samples=500)
        pixelated_points = self.snap_to_grid(original_points, pixel_size=self.pixelation_level)

        buffer = io.BytesIO()
        self.build_and_save_plot(original_points, pixelated_points, buffer)

        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return image_base64
