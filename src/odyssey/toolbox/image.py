import os
from PIL import Image


def image_resize(imagefile, type, size):
    save = False
    _file = os.path.basename(imagefile)
    _dir = os.path.join(os.path.dirname(imagefile), type + size)
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    filename = os.path.join(_dir, _file)
    try:
        if os.path.exists(filename):
            return filename
        size = int(size)
        source = Image.open(imagefile)
        if type == 'w':
            if source.size[0] > size:
                wpercent = (size/float(source.size[0]))
                hsize = int((float(source.size[1])*float(wpercent)))
                source = source.resize((size, hsize), Image.ANTIALIAS)
            save = True
        elif type == 'h':
            if source.size[1] > size:
                wpercent = (size/float(source.size[1]))
                hsize = int((float(source.size[0])*float(wpercent)))
                source = source.resize((hsize, size), Image.ANTIALIAS)
            save = True
        elif type == 's':
            if source.size[0] < source.size[1]:
                wpercent = (size/float(source.size[0]))
                hsize = int((float(source.size[1])*float(wpercent)))
                source = source.resize((size, hsize), Image.ANTIALIAS)
                left = 0
                top = int((source.size[1]/2)-(size/2))
                right = size
                bottom = int((source.size[1]/2)+(size/2))
                source = source.crop((left, top, right, bottom))
                save = True
            else:
                wpercent = (size/float(source.size[1]))
                hsize = int((float(source.size[0])*float(wpercent)))
                source = source.resize((hsize, size), Image.ANTIALIAS)
                left = int((source.size[0]/2)-(size/2))
                top = 0
                right = int((source.size[0]/2)+(size/2))
                bottom = size
                source = source.crop((left, top, right, bottom))
                save = True
        if save:
            source.save(filename)
            return filename
        else:
            return False
    except:
        return False


def what(file, h=None):
    f = None
    try:
        if h is None:
            if isinstance(file, str):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return True
    finally:
        if f: f.close()
    return None


tests = []


def test_jpeg(h, f):
    """JPEG data in JFIF format"""
    if h[6:10] == b'JFIF':
        return 'jpeg'

tests.append(test_jpeg)


def test_exif(h, f):
    """JPEG data in Exif format"""
    if h[6:10] == b'Exif':
        return 'jpeg'

tests.append(test_exif)


def test_png(h, f):
    if h[:8] == b"\x89PNG\r\n\032\n":
        return 'png'

tests.append(test_png)


def test_gif(h, f):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

tests.append(test_gif)


def test_tiff(h, f):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b'MM', b'II'):
        return 'tiff'

tests.append(test_tiff)


def test_rgb(h, f):
    """SGI image library"""
    if h[:2] == b'\001\332':
        return 'rgb'

tests.append(test_rgb)


def test_pbm(h, f):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and \
        chr(h[0]) == 'P' and chr(h[1]) in '14' and chr(h[2]) in ' \t\n\r':
        return 'pbm'

tests.append(test_pbm)


def test_pgm(h, f):
    """PGM (portable graymap)"""
    if len(h) >= 3 and \
        chr(h[0]) == 'P' and chr(h[1]) in '25' and chr(h[2]) in ' \t\n\r':
        return 'pgm'

tests.append(test_pgm)


def test_ppm(h, f):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and \
        chr(h[0]) == 'P' and chr(h[1]) in '36' and chr(h[2]) in ' \t\n\r':
        return 'ppm'

tests.append(test_ppm)


def test_rast(h, f):
    """Sun raster file"""
    if h[:4] == b'\x59\xA6\x6A\x95':
        return 'rast'

tests.append(test_rast)


def test_xbm(h, f):
    """X bitmap (X10 or X11)"""
    s = '#define '
    if h[:len(s)] == s:
        return 'xbm'

tests.append(test_xbm)


def test_bmp(h, f):
    if h[:2] == b'BM':
        return 'bmp'

tests.append(test_bmp)
