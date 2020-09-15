from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
# Create your models here.


def generate_unique_slug(klass, field):
    slug = field
    numb = 1
    while klass.objects.filter(slug=slug).exists():
        slug = '%s-%d' % ("-".join(slug.split()), numb)
        numb += 1

    return slug


class Location(models.Model):
    DIVISION_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Rajshahi', 'Rajshahi')
    )
    division = models.CharField(max_length=200, choices=DIVISION_CHOICES)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = '1. Location'

    def __str__(self):
        return f"{self.city} --> {self.area}"


class Package(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='packages')
    price = models.FloatField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = '2. Package'

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Package, self.title)
        else:
            self.slug = generate_unique_slug(Package, self.title)
        super(Package, self).save(*args, **kwargs)

    @property
    def total_day(self):
        return self.end_date - self.start_date

    def __str__(self):
        return self.title


class PackageImage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="package")

    class Meta:
        verbose_name = 'Package Image'
        verbose_name_plural = '3. Package Images'

    def image_tag(self):
        return mark_safe(f"<img src='/media/{self.image}' width='150' height='150' />")

    image_tag.short_description = 'View Image'

    def __str__(self):
        return self.package.title


class PackageSchedule(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Package Schedule'
        verbose_name_plural = '4. Package Schedule'

    def __str__(self):
        return self.package.title


class PackageExtra(models.Model):
    EXTRA_CHOICES = (
        ('1', 'Avialable'),
        ('2', 'Not Avialable'),
        ('3', 'May Be')
    )

    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='extras')
    name = models.CharField(max_length=255)
    avialable = models.CharField(max_length=10, choices=EXTRA_CHOICES)

    class Meta:
        verbose_name = 'Package Extra'
        verbose_name_plural = '5. Package Extra'

    def __str__(self):
        return self.package.title


class PackageVideo(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='videos')
    link = models.URLField()

    class Meta:
        verbose_name = 'Package Video'
        verbose_name_plural = '6. Package Videos'

    def __str__(self):
        return self.package.title
