from django.urls import path
from .views import ProductDetailView, ProductCreateView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    # Add other product-related URLs as needed
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]