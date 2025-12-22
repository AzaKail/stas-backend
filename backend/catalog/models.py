from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=80, unique=True)   # iPhone, MacBook...
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    brand = models.CharField(max_length=50, default="Apple")

    description = models.TextField(blank=True)
    warranty = models.CharField(max_length=100, blank=True, default="")

    is_visible = models.BooleanField(default=True)   # “Товар видимый”
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")

    cover = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)

    memory_gb = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=80, blank=True, default="")

    price = models.IntegerField()
    old_price = models.IntegerField(null=True, blank=True)   # “старая цена”
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        mem = f"{self.memory_gb}GB" if self.memory_gb else "-"
        return f"{self.product.title} / {mem} / {self.color} / {self.price}"
