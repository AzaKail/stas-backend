from rest_framework import serializers
from .models import Product, Variant

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "memory_gb", "color", "price", "in_stock"]

class ProductListSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "category", "brand", "cover", "min_price", "warranty"]

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "category", "brand", "description", "warranty", "cover", "variants"]

