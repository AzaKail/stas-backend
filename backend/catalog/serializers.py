from rest_framework import serializers
from .models import Product, Variant, Tag

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "memory_gb", "color", "price", "in_stock"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["slug", "title", "group"]

class ProductListSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField()
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "category", "brand", "cover", "min_price", "warranty", "tags"]

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "category", "brand", "description", "warranty", "cover", "variants", "tags"]