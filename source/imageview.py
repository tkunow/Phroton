import cv2
import numpy
from custom_types import Rotation

class ImageView:
    def _convertBGR2RGB(self, image) -> cv2.typing.MatLike:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def save_image(self, name: str, image) -> None:
        bgr_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if not cv2.imwrite(name, bgr_img):
            raise SystemError(f"Could not save image: {name}")

    def read_image(self, path: str, mode: int = cv2.IMREAD_COLOR) -> cv2.typing.MatLike:
        img = cv2.imread(path, mode)
    
        if img is None:
            raise FileNotFoundError(f"Could not decode image: {path}")
        return self._convertBGR2RGB(img)

    def rotate_image(self, image, direction: Rotation) -> cv2.typing.MatLike:
        height, width = image.shape[:2]
        center = (width/2, height/2)

        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=direction.value, scale=1)
        return cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    def zoom_image(self, image, factor: float) -> cv2.typing.MatLike:
        factor = max(0.01, factor)
        if factor == 1.0:
            return image

        height, width = image.shape[:2]
        scaled_width = max(1, int(width * factor))
        scaled_height = max(1, int(height * factor))
        return cv2.resize(image, (scaled_width, scaled_height), interpolation=cv2.INTER_LINEAR)

    def draw_watermark(self, image, text:str) -> cv2.typing.MatLike:
        thickness = 5
        opacity = 0.5
        height, width= image.shape[:2]
        scale = self._calc_text_scale(text, width, thickness, 1)
        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, scale, thickness)[0]
        text_location = (int(width - size[0]), int(height + size[1]))
        center = (width/2, height/2)

        watermark_mask = numpy.zeros((height, width), numpy.uint8)
        cv2.putText(
            img=watermark_mask,
            text=text,
            org=(int(text_location[0] / 2),
                int(text_location[1] / 2)),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=scale,
                color=255,
                thickness=5,
                lineType=cv2.LINE_AA,
            )

        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=45, scale=1)
        watermark_mask = cv2.warpAffine(
            src=watermark_mask,
            M=rotate_matrix,
            dsize=(width, height),
            flags=cv2.INTER_LINEAR,
        )

        alpha = (watermark_mask.astype(numpy.float32) / 255.0) * opacity
        alpha = alpha[:, :, numpy.newaxis]
        watermark_color = numpy.full_like(image, 125)
        blended = image.astype(numpy.float32) * (1.0 - alpha) + watermark_color * alpha
        return blended.astype(image.dtype)

    def _draw_rectangle(self, image, p1, p2, thickness: int, color: tuple[int, int, int] = (0,0,255)) -> cv2.typing.MatLike:
        image_with_rectangle = image.copy()
        return cv2.rectangle(image_with_rectangle, p1, p2, color, thickness)

    def _draw_circle(self, image, p1, p2, thickness: int) -> cv2.typing.MatLike:
        image_with_circle = image.copy()
        return cv2.circle(image_with_circle, p1, p2, (0,0,255), thickness)

    def _draw_line(self, image, p1, radius, thickness:int) -> cv2.typing.MatLike:
        image_with_line = image.copy()
        return cv2.line(image_with_line, p1, radius, (0,0,255), thickness)

    def _calc_text_scale(self, text:str, width: int, thickness:int, scale:float = 1) -> float:
        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, scale, thickness)[0]

        if size[0] >= width:
            return scale

        return self._calc_text_scale(text, width, thickness, scale + 0.1)
