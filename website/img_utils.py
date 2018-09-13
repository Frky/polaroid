
from PIL import Image as IMG
from PIL import ExifTags

from django.core.files.base import ContentFile, BytesIO


def resize(image, max_len):
    w, h = image.size
    if w < h:
        nh = min(max_len, h)
        nw = w * (nh / float(h)) 
    else:
        nw = min(max_len, w)
        nh = h * (nw / float(w)) 
    medium = image.resize((int(nw), int(nh)), IMG.ANTIALIAS)
    buffer = BytesIO()
    medium.save(buffer, image.format, quality=100)
    return ContentFile(buffer.getvalue())


def rotate(raw_img, fmt):
    """
        Rotate the image with PIL if the Orientation Exif tag is set

        @param raw_img      the raw content of the image to rotate if needed
        @param fmt          the image format

        @ret                a new raw content

    """
    img = IMG.open(raw_img)
    try:
        orientation = next(filter(lambda a: a[1] == "Orientation", ExifTags.TAGS.items()))[0]
        exif=dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError) as e:
        # No Orientation exif tag
        pass
    buffer = BytesIO()
    img.save(buffer, fmt, quality=100)
    return ContentFile(buffer.getvalue())

