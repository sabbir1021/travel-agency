from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.conf import settings

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
    division = models.CharField(max_length=200, choices=DIVISION_CHOICES , blank=True)
    city = models.CharField(max_length=100 )
    place = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Location Image")

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = '1. Location'
    
    def save(self, *args, **kwargs):
        self.city = self.city.lower()
        return super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.city


class Package(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='packages')
    price = models.FloatField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    special = models.BooleanField(default=False)

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
        return str(self.end_date - self.start_date)

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


class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return str(self.name)

class Clientfeedback(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    message = models.TextField()
    image = models.ImageField(upload_to="Clinet feedback")
    rating = models.IntegerField(default=True)

    def __str__(self):
        return str(self.name)


class ProductQuerySet(models.QuerySet):
    def price_filter(self, price, last_price=None):
        print(price, last_price)
        if last_price:
            print(last_price)
            return self.filter(price__gte=last_price)
        return self.filter(price__range=(0, price))

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def price_filter(self, price, last_price):
        return self.get_queryset().price_filter(price, last_price)


    
   