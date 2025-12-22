from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("iPhone", "iPhone"),
        ("MacBook", "MacBook"),
        ("iPad", "iPad"),
        ("Watch", "Watch"),
        ("AirPods", "AirPods"),
        ("Huawei", "Huawei"),
        ("Dyson", "Dyson"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=50, default="Apple")
    description = models.TextField(blank=True)
    warranty = models.CharField(max_length=100, blank=True, default="")

    # можно ImageField, можно URL — оставлю ImageField:
    cover = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.title


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)

    memory_gb = models.IntegerField(null=True, blank=True)   # 128/256/512...
    color = models.CharField(max_length=80, blank=True, default="")
    price = models.IntegerField()                            # в рублях
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        mem = f"{self.memory_gb}GB" if self.memory_gb else "-"
        return f"{self.product.title} / {mem} / {self.color} / {self.price}"
