"""Unit tests for image loading and transformation helpers."""

from pathlib import Path
import sys
import tempfile
import unittest

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "source"))

from custom_types import Rotation  # noqa: E402
from imageview import ImageView  # noqa: E402


class ImageViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.image_view = ImageView()

    def test_convert_bgr_to_rgb_swaps_colour_channels(self) -> None:
        bgr_image = np.array([[[10, 20, 30]]], dtype=np.uint8)

        rgb_image = self.image_view._convertBGR2RGB(bgr_image)

        np.testing.assert_array_equal(
            rgb_image, np.array([[[30, 20, 10]]], dtype=np.uint8)
        )

    def test_read_image_returns_rgb_image(self) -> None:
        bgr_image = np.array([[[5, 15, 25]]], dtype=np.uint8)
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "sample.png"
            self.assertTrue(cv2.imwrite(str(image_path), bgr_image))

            image = self.image_view.read_image(str(image_path))

        np.testing.assert_array_equal(
            image, np.array([[[25, 15, 5]]], dtype=np.uint8)
        )

    def test_read_image_raises_for_missing_or_invalid_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.png"

            with self.assertRaises(FileNotFoundError):
                self.image_view.read_image(str(missing_path))

    def test_rotate_image_preserves_dimensions_and_changes_orientation(self) -> None:
        image = np.zeros((5, 5, 3), dtype=np.uint8)
        image[2, 1] = [255, 0, 0]

        rotated_left = self.image_view.rotate_image(image, Rotation.LEFT)
        rotated_right = self.image_view.rotate_image(image, Rotation.RIGHT)

        self.assertEqual(rotated_left.shape, image.shape)
        self.assertEqual(rotated_right.shape, image.shape)
        self.assertFalse(np.array_equal(rotated_left, image))
        self.assertFalse(np.array_equal(rotated_right, image))
        self.assertFalse(np.array_equal(rotated_left, rotated_right))

    def test_zoom_image_returns_original_at_one_times_scale(self) -> None:
        image = np.zeros((4, 6, 3), dtype=np.uint8)

        zoomed_image = self.image_view.zoom_image(image, 1.0)

        self.assertIs(zoomed_image, image)

    def test_zoom_image_resizes_image_for_positive_scale(self) -> None:
        image = np.zeros((4, 6, 3), dtype=np.uint8)

        zoomed_image = self.image_view.zoom_image(image, 2.0)

        self.assertEqual(zoomed_image.shape, (8, 12, 3))

    def test_zoom_image_clamps_zero_scale_to_minimum_size(self) -> None:
        image = np.zeros((4, 6, 3), dtype=np.uint8)

        zoomed_image = self.image_view.zoom_image(image, 0.0)

        self.assertEqual(zoomed_image.shape, (1, 1, 3))


if __name__ == "__main__":
    unittest.main()
