
import os 
from PIL import Image as PILImage

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from website.random_primary import RandomPrimaryIdModel

def image_path(instance, filename, size):
    print(instance.id)
    ext = os.path.splitext(filename)[1]
    return '{0}/{1}{2}{3}'.format(instance.gl.path, instance.id, size, ext)

def image_large_path(instance, filename):
    return image_path(instance, filename, '-large')

def image_normal_path(instance, filename):
    return image_path(instance, filename, '')

def image_thumb_path(instance, filename):
    return image_path(instance, filename, '-small')

class Gallery(RandomPrimaryIdModel):
    # Name of the gallery
    name = models.CharField(max_length=256, blank=True, null=True)
    path = models.CharField(max_length=1024, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ForeignKey('Image', null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        super(Gallery, self).save(*args, **kwargs)
        # Create the repo for this gallery
        path = os.path.join(settings.MEDIA_ROOT, self.id)
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        super(Gallery, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isdir(self.path):
            os.remove(self.path)
        super(Gallery, self).delete(*args,**kwargs)

class Image(RandomPrimaryIdModel):
    path = models.ImageField(upload_to=image_normal_path, blank=True, null=True)
    large = models.ImageField(upload_to=image_large_path, blank=True, null=True)
    thumb = models.ImageField(upload_to=image_thumb_path, blank=True, null=True)
    caption = models.CharField(max_length=1024, null=True, blank=True, default="")
    uploaded = models.DateTimeField(auto_now_add=True)
    gl = models.ForeignKey('Gallery', null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def crop(self, r):
        for img in [self.path, self.thumb]:
            im = PILImage.open(img)
            cropped = im.copy()
            h, w = cropped.height, cropped.width
            if h < w:
                nh = w / r
                p = int((h - nh) / 2)
                cropped = cropped.crop((0, p, w, h - p))
            cropped.save(str(img), im.format)
            im.close()

    def delete(self, *args, **kwargs):
        if self.path and os.path.isfile(self.path.path):
            os.remove(self.path.path)
        if self.large and os.path.isfile(self.large.path):
            os.remove(self.large.path)
        if self.thumb and os.path.isfile(self.thumb.path):
            os.remove(self.thumb.path)

        super(Image, self).delete(*args,**kwargs)
