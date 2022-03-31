from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Gallery)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(SizeTable)
admin.site.register(ColorTable)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
