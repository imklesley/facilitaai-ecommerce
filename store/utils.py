from django.shortcuts import redirect

import json

from .models import Product, Color, Size, Order


def cookie_cart(request):
    cookies = request.COOKIES
    # print(cookies)
    # Verifica-se se o cookie cart existe na request, se não existe seta
    # cookie cart para {}
    try:
        cookie_cart = json.loads(cookies['cart'])
    except KeyError:
        cookie_cart = {}
    # print(cookie_cart)

    order = {'orderitem_set': {'all': [], 'count': 0, },
                'quantity_items': 0, 'total_price': 0}

    for cart_item in cookie_cart.values():
        product = Product.objects.get(id=cart_item['product_id'])
        color = Color.objects.get(id=cart_item['color_id'])
        size = Size.objects.get(id=cart_item['size_id'])

        item = {'product': product, 'size': size,
                'color': color, 'quantity': cart_item['quantity'], }

        order['orderitem_set']['all'].append(item)

        order['orderitem_set']['count'] += 1
        order['quantity_items'] += cart_item['quantity']
        order['total_price'] += cart_item['quantity'] * product.price

    return order



def cart_data(request):
    user = request.user

    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, on_cart=True)

    else:
        order = cookie_cart(request=request)
    

    return order



    