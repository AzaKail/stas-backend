from django.urls import path
from .views import ProductListView, ProductDetailView, FiltersView

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<slug:slug>/", ProductDetailView.as_view()),
    path("filters/", FiltersView.as_view()),
]
