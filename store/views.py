from django.shortcuts import render

from .models import Product, Order


# Create your views here.

def home(request):
    context = {}

    products = Product.objects.all()

    context['products'] = products

    return render(request, 'store/home.html', context)


def cart(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, on_cart=True)

    else:
        order = Order()

    context['order'] = order

    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, on_cart=True)

    else:
        order = Order()

    context['order'] = order

    return render(request, 'store/checkout.html', context)
