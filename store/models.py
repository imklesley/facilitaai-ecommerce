from django.db import models

from django.contrib.auth.models import User

from datetime import datetime


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def has_address(self):

        return self.shippingaddress != None


class Gallery(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    @property
    def cover(self):
        product_image = ProductImage.objects.filter(gallery_id=self.id).first()
        return product_image


def upload_location(instance, filename, *args, **kwargs):
    now = datetime.now()
    file_path = f'products/{instance.gallery.name}/{now.microsecond}-{filename}'
    return file_path


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    about = models.CharField(max_length=200, null=True, blank=False)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.gallery.name} - {self.id}'


class ColorTable(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Color(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    hex_color = models.CharField(max_length=7, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    color_table = models.ForeignKey(ColorTable, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.color_table.name} - {self.name} - {self.id}'

    @property
    def quantity_items_by_color(self):
        colors = self.color_table.color_set.all()

        quantity = 0
        for color in colors:
            quantity += color.quantity

        return quantity


class SizeTable(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    size_table = models.ForeignKey(SizeTable, null=False, blank=False, on_delete=models.CASCADE)
    color_table = models.ForeignKey(ColorTable, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.size_table.name} - {self.name}'

    @property
    def available_colors(self):
        colors = self.color_table.color_set.filter(color_table=self.color_table)
        # print(colors)
        return colors


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    old_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    visible = models.BooleanField(default=True, null=False, blank=False)

    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)

    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE)

    size_table = models.OneToOneField(SizeTable, null=False, blank=False, on_delete=models.CASCADE)

    # color_table = models.OneToOneField(ColorTable, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    PROCESSING_PAYMENT = 'PP'
    SEPARATING_PRODUCTS = 'SP'
    OUT_FOR_DELIVERY = 'OFD'
    PRODUCTS_DELIVERED = 'PD'

    STATUS = ((PROCESSING_PAYMENT, 'Processing Payment'), (SEPARATING_PRODUCTS, 'Separating Products'),
              (OUT_FOR_DELIVERY, 'Out For Delivery'), (PRODUCTS_DELIVERED, 'Products Delivered'))

    customer = models.ForeignKey(Customer, null=True, blank=False, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    on_cart = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        # order_items = OrderItem.objects.filter(order_id=self.id)
        order_items = self.orderitem_set.filter(order_id=self.id)
        total = 0
        for item in order_items:
            total += item.price * item.quantity

        return total

    @property
    def quantity_items(self):
        order_items = OrderItem.objects.filter(order_id=self.id)
        quantity = 0
        for item in order_items:
            quantity += item.quantity

        return quantity


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, blank=False, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order  {self.order.id} - {self.product.name}'


class ShippingAddress(models.Model):
    customer = models.OneToOneField(Customer, null=True, blank=False, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=250, blank=False, null=False)
    zipcode = models.CharField(max_length=30, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
