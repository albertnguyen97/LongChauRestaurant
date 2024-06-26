"""chaulong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('warehouse/', include('warehouse.urls')),  # Replace 'your_app' with your actual app name
    path('cart/', include('cart.urls', namespace='cart')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('order-cart/', include('order_cart.urls', namespace='order_cart')),
    path('', include('restaurant.urls')),
    path('api/', include('chaulongAPI.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('eat-in/', include('eat_in_restaurant.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('rosetta/', include('rosetta.urls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)