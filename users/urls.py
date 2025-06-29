from django.urls import path
from .views import custom_login_view, custom_logout_view, RegisterView, home_view,user_profile_view,update_product_status,search_results_view,category_products

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),  # 👈 Accessing the class-based view
    path('home/', home_view, name='home'),
    path('profile',user_profile_view,name='profile'),
    path('product/<int:pk>/update-status/', update_product_status, name='update_product_status'),
    path('search/', search_results_view, name='search_results'),
    path('category/<str:category_name>/', category_products, name='category_products'),
]
