"""
URL configuration for slayyanna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Redirect the base URL to the login page
    path('', RedirectView.as_view(url='/users/login/', permanent=True)),

    # Include the URLs from the users app
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),

    # You can include other app URLs similarly:
    # path('products/', include('products.urls')),
    # etc.
    path('messages/', include('messaging.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('donations/', include('donations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

