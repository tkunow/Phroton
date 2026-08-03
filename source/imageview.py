import cv2
from custom_types import Rotation

class ImageView:
    def convertBGR2RGB(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def readImage(self, path: str, mode: int = cv2.IMREAD_COLOR):
        img = cv2.imread(path, mode)
    
        if img is None:
            raise FileNotFoundError(f"Could not decode image: {path}")
        return self.convertBGR2RGB(img)

    def rotateImage(self, image, direction: Rotation):
        height, width = image.shape[:2]
        center = (width/2, height/2)

        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=direction.value, scale=1)
        return cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    def zoomImage(self, image, factor: float):
        factor = max(0.01, factor)
        if factor == 1.0:
            return image

        height, width = image.shape[:2]
        scaled_width = max(1, int(width * factor))
        scaled_height = max(1, int(height * factor))
        return cv2.resize(image, (scaled_width, scaled_height), interpolation=cv2.INTER_LINEAR)

