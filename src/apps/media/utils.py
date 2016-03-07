from PIL import Image, ImageDraw, ImageFont
from .settings import *


def create_icon(filename):
    img = Image.new('RGB', (ICON_FILE_SIZE, ICON_FILE_SIZE), ICON_FILE_COLOR)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(ICON_FONT1, ICON_FONT_SIZE)
    text = os.path.basename(filename).replace('.' + os.path.basename(filename).split('.')[-1], '')
    i = 1
    while font.getsize(text)[0] > ICON_TEXT_SIZE:
        font = ImageFont.truetype(ICON_FONT1, ICON_FONT_SIZE - i)
        i += 1
    draw.text(((ICON_FILE_SIZE/2)-font.getsize(text)[0]/2, ICON_TEXT_ROW1), text, ICON_TEXT_COLOR, font=font)

    font = ImageFont.truetype(ICON_FONT2, ICON_FONT_SIZE)
    text = filename.split(".")[-1]
    i = 1
    while font.getsize(text)[0] > ICON_TEXT_SIZE:
        font = ImageFont.truetype(ICON_FONT2, ICON_FONT_SIZE - i)
        i += 1
    draw.text(((ICON_FILE_SIZE/2)-font.getsize(text)[0]/2, ICON_TEXT_ROW2), text, ICON_TEXT_COLOR, font=font)

    img.save(os.path.join(os.path.dirname(filename), ICON_FILE_NAME))
