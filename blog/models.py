from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="category")
    title = models.CharField(max_length=220)
    description = RichTextField()
    image = models.ImageField(upload_to="blog")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.compressImage(self.image)
        super(Post, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='PNG', quality=60)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.png" % image.name.split('.')[
            0], 'image/png', sys.getsizeof(outputIoStream), None)
        return image
