import random
from io import BytesIO as StringIO
from PIL import Image, ImageDraw, ImageFont
from config import CAPTCHA_CHARS, CAPTCHA_COLORS, CAPTCHA_FONT_PATH, CAPTCHA_FONT_SIZE, \
    CAPTCHA_LETTER_ROTATION_LEFT, CAPTCHA_LETTER_ROTATION_RIGHT


def captcha_code(size):
    return ''.join(random.choice(CAPTCHA_CHARS) for x in range(size))


def captcha_image(text, scale=1):
    if CAPTCHA_FONT_PATH.lower().strip().endswith('ttf'):
        font = ImageFont.truetype(CAPTCHA_FONT_PATH, CAPTCHA_FONT_SIZE * scale)
    else:
        font = ImageFont.load(CAPTCHA_FONT_PATH)

    size = font.getsize(text)
    size = (size[0] * 2, 50)
    image = Image.new('RGBA', size)

    xpos = 2

    charlist = []
    for char in text:
            charlist.append(char)
    for char in charlist:
        fgimage = Image.new('RGB', size, random.choice(CAPTCHA_COLORS))
        fsize = (50, 50)
        charimage = Image.new('L', fsize, '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')

        charimage = charimage.rotate(random.randrange(CAPTCHA_LETTER_ROTATION_LEFT, CAPTCHA_LETTER_ROTATION_RIGHT),
                                     expand=0, resample=Image.BICUBIC)
        charimage = charimage.crop(charimage.getbbox())
        maskimage = Image.new('L', size)

        maskimage.paste(charimage, (xpos, 4, xpos + charimage.size[0], 4 + charimage.size[1]))
        size = maskimage.size
        image = Image.composite(fgimage, image, maskimage)
        xpos = xpos + 2 + charimage.size[0]

    image = image.crop((0, 0, xpos + 1, size[1]))

    out = StringIO()
    image.save(out, "PNG")
    out.seek(0)
    return out
