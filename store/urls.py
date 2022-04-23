from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/', update_cart, name='update_cart'),
    path('process_order/', process_order, name='process_order'),
    path('process_order_whatsapp/', process_order_whatsapp, name='process_order_whatsapp'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
