from django.urls import path
from products.views import get_product
from products.views import add_to_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('<slug>/', get_product, name='get_product'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('<slug>/add_to_cart/', add_to_cart, name='add_to_cart')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)