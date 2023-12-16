from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.name