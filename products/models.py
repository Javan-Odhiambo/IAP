from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Product(models.Model):
    """Model definition for Product."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Model definition for ProductImage."""

    image = models.ImageField(upload_to="products")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name}-{self.image}"


class Variant(models.Model):
    """Model definition for Variant."""

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    size = models.ForeignKey("products.ProductSize", on_delete=models.CASCADE)
    color = models.ForeignKey("products.ProductColor", on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
        unique_together = ["product", "size", "color"]

    def save(self, *args, **kwargs):
        self.is_available = self.stock_quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name}-{self.size}-{self.color}"


class ProductSize(models.Model):
    """Model definition for ProductSize."""

    value = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        self.value = self.value.lower()
        super().save(*args, **kwargs)


class ProductColor(models.Model):
    """Model definition for ProductColor."""

    value = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        self.value = self.value.lower()
        super().save(*args, **kwargs)


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    """Model definition for Review."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ["user", "product"]
