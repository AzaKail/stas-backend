from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Category, Tag, Product, Variant


# --- SERIALIZERS ---
class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "order"]


class TagAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", "slug"]


class VariantAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "product", "memory_gb", "color", "price", "old_price", "in_stock"]


class ProductAdminSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id", "title", "slug", "category", "brand", "description", "warranty",
            "is_visible", "cover", "tags",
        ]


# --- VIEWSETS ---
class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("order", "title")
    serializer_class = CategoryAdminSerializer
    permission_classes = [IsAdminUser]


class TagAdminViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("title")
    serializer_class = TagAdminSerializer
    permission_classes = [IsAdminUser]


class ProductAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        qs = Product.objects.all().select_related("category").prefetch_related("tags")
        category_id = self.request.query_params.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs.order_by("id")


class VariantAdminViewSet(viewsets.ModelViewSet):
    serializer_class = VariantAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Variant.objects.all().select_related("product")
        product_id = self.request.query_params.get("product")
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs.order_by("id")
