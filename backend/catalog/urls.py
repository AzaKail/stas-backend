from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductListView, ProductDetailView, FiltersView
from .admin_api import CategoryAdminViewSet, TagAdminViewSet, ProductAdminViewSet, VariantAdminViewSet

router = DefaultRouter()
router.register(r"admin/categories", CategoryAdminViewSet, basename="admin-categories")
router.register(r"admin/tags", TagAdminViewSet, basename="admin-tags")
router.register(r"admin/products", ProductAdminViewSet, basename="admin-products")
router.register(r"admin/variants", VariantAdminViewSet, basename="admin-variants")

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<slug:slug>/", ProductDetailView.as_view()),
    path("filters/", FiltersView.as_view()),
]

urlpatterns += router.urls
