from django.contrib import admin
from .models import Category, Tag, Product, Variant, ProductImage

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order")
    list_editable = ("order",)
    search_fields = ("title", "slug")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "brand", "is_visible")
    list_filter = ("category", "brand", "is_visible", "tags")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [VariantInline, ProductImageInline]
