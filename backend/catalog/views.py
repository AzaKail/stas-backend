from django.db.models import Min, Max, Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Variant, Tag, Category
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        # Показываем только видимые товары (если поле is_visible есть)
        qs = Product.objects.filter(is_visible=True).select_related("category")

        q = self.request.query_params.get("q")
        category = self.request.query_params.get("category")  # ожидаем slug категории
        brand = self.request.query_params.get("brand")

        memories = self.request.query_params.getlist("memory")  # ?memory=256&memory=512
        colors = self.request.query_params.getlist("color")     # ?color=Midnight
        tags = self.request.query_params.getlist("tag")         # ?tag=esim&tag=new

        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if category:
            qs = qs.filter(category__slug=category)

        if brand:
            qs = qs.filter(brand=brand)

        if tags:
            qs = qs.filter(tags__slug__in=tags)

        # фильтры по вариантам
        if memories:
            qs = qs.filter(variants__memory_gb__in=memories)

        if colors:
            qs = qs.filter(variants__color__in=colors)

        if price_min:
            qs = qs.filter(variants__price__gte=int(price_min))

        if price_max:
            qs = qs.filter(variants__price__lte=int(price_max))

        # "Цена от"
        qs = qs.annotate(min_price=Min("variants__price")).distinct().order_by("min_price")
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class FiltersView(APIView):
    """
    Возвращает доступные значения фильтров.
    """
    def get(self, request):
        category = request.query_params.get("category")  # slug категории
        brand = request.query_params.get("brand")

        variants = Variant.objects.select_related("product", "product__category").filter(
            product__is_visible=True
        )

        if category:
            variants = variants.filter(product__category__slug=category)

        if brand:
            variants = variants.filter(product__brand=brand)

        memories = list(
            variants.exclude(memory_gb__isnull=True)
                    .order_by("memory_gb")
                    .values_list("memory_gb", flat=True)
                    .distinct()
        )

        colors = list(
            variants.exclude(color="")
                    .order_by("color")
                    .values_list("color", flat=True)
                    .distinct()
        )

        min_price = variants.aggregate(mn=Min("price"))["mn"] or 0
        max_price = variants.aggregate(mx=Max("price"))["mx"] or 0

        # Категории лучше брать из таблицы Category
        categories = list(
            Category.objects.order_by("order", "title").values("title", "slug")
        )

        brands = list(
            Product.objects.filter(is_visible=True)
                   .values_list("brand", flat=True)
                   .distinct()
                   .order_by("brand")
        )

        # ✅ Вот так получаем список тегов
        tags = list(
            Tag.objects.order_by("title").values("title", "slug")
        )

        # ✅ И вот так добавляем их в Response
        return Response({
            "categories": categories,
            "brands": brands,
            "tags": tags,  # <-- ВОТ ЭТО
            "memories": memories,
            "colors": colors,
            "price": {"min": min_price, "max": max_price},
        })
