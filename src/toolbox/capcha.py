import re
import os
import random
from django.http import HttpResponse
from odyssey.settings import STATICFILES_DIRS


try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import Image
    import ImageDraw
    import ImageFont

try:
    import json
except ImportError:
    from django.utils import simplejson as json


CAPTCHA_FONT_SIZE = 42
CAPTCHA_LETTER_ROTATION_LEFT = -35
CAPTCHA_LETTER_ROTATION_RIGHT = 35
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_BACKGROUND_COLOR_TRANSPARENT = (255, 0, 0, 0)
CAPTCHA_FOREGROUND_COLOR = '#001100'

NON_DIGITS_RX = re.compile('[^\d]')


def capcha_code(size):
    return ''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for x in range(size))


def capcha_dark_color():
    c = ['#00267C', '#AF0000', '#3400C4', '#005089', '#347F3D',
         '#CE9300', '#282828', '#580082', '#008E8E', '#A84300']
    return random.choice(c)


def captcha_image(text, scale=1):
    CAPTCHA_FONT_PATH = os.path.normpath(
        os.path.join(os.path.join(STATICFILES_DIRS[0], 'fonts'), 'sketch_2.ttf'))

    if CAPTCHA_FONT_PATH.lower().strip().endswith('ttf'):
        font = ImageFont.truetype(CAPTCHA_FONT_PATH, CAPTCHA_FONT_SIZE * scale)
    else:
        font = ImageFont.load(CAPTCHA_FONT_PATH)

    size = font.getsize(text)
    size = (size[0] * 2, 50)
    image = Image.new('RGBA', size)

    try:
        PIL_VERSION = int(NON_DIGITS_RX.sub('', Image.VERSION))
    except:
        PIL_VERSION = 116
    xpos = 2

    charlist = []
    for char in text:
        charlist.append(char)
    for char in charlist:
        fgimage = Image.new('RGB', size, capcha_dark_color())
        fsize = (50, 50)
        charimage = Image.new('L', fsize, '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')

        if PIL_VERSION >= 116:
            charimage = charimage.rotate(random.randrange(CAPTCHA_LETTER_ROTATION_LEFT, CAPTCHA_LETTER_ROTATION_RIGHT),
                                         expand=0, resample=Image.BICUBIC)
        else:
            charimage = charimage.rotate(random.randrange(CAPTCHA_LETTER_ROTATION_LEFT, CAPTCHA_LETTER_ROTATION_RIGHT),
                                         resample=Image.BICUBIC)
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

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    return response
