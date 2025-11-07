from PIL import ImageFont
import os

def load_font(font: str, size: int = 32):
    font_path = os.path.join("fonts", font)
    if os.path.exists(font_path):
        return ImageFont.truetype(font=font_path, size=size)
    return ImageFont.truetype(font=font, size=size)
