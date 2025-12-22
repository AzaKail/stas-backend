from django.db.models import Min, Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Variant
from .serializers import ProductListSerializer, ProductDetailSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.all()

        q = self.request.query_params.get("q")
        category = self.request.query_params.get("category")
        brand = self.request.query_params.get("brand")

        memories = self.request.query_params.getlist("memory")  # ?memory=256&memory=512
        colors = self.request.query_params.getlist("color")     # ?color=Midnight...
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if category:
            qs = qs.filter(category=category)

        if brand:
            qs = qs.filter(brand=brand)

        # фильтры по вариантам
        if memories:
            qs = qs.filter(variants__memory_gb__in=memories)

        if colors:
            qs = qs.filter(variants__color__in=colors)

        if price_min:
            qs = qs.filter(variants__price__gte=int(price_min))

        if price_max:
            qs = qs.filter(variants__price__lte=int(price_max))

        # аннотация "цена от"
        qs = qs.annotate(min_price=Min("variants__price")).distinct().order_by("min_price")
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class FiltersView(APIView):
    """
    Возвращает доступные значения фильтров в рамках категории/поиска.
    """
    def get(self, request):
        category = request.query_params.get("category")
        brand = request.query_params.get("brand")

        variants = Variant.objects.select_related("product")

        if category:
            variants = variants.filter(product__category=category)
        if brand:
            variants = variants.filter(product__brand=brand)

        memories = list(
            variants.exclude(memory_gb__isnull=True).order_by("memory_gb").values_list("memory_gb", flat=True).distinct()
        )
        colors = list(
            variants.exclude(color="").order_by("color").values_list("color", flat=True).distinct()
        )
        min_price = variants.aggregate(m=Min("price"))["m"] or 0
        max_price = variants.aggregate(m=Min("price"))["m"] or 0  # поправим ниже

        # max отдельно
        from django.db.models import Max
        max_price = variants.aggregate(mx=Max("price"))["mx"] or 0

        categories = list(Product.objects.values_list("category", flat=True).distinct().order_by("category"))
        brands = list(Product.objects.values_list("brand", flat=True).distinct().order_by("brand"))

        return Response({
            "categories": categories,
            "brands": brands,
            "memories": memories,
            "colors": colors,
            "price": {"min": min_price, "max": max_price},
        })
