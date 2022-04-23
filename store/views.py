from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404


from .models import Product, Order, OrderItem, Color
from store.utils import cart_data


def home(request):
    context = {}

    context['order'] = cart_data(request=request)

    # TODO: Fazer paginação
    products = Product.objects.all()
    context['products'] = products

    return render(request, 'store/home.html', context)


def cart(request):
    context = {}

    context['order'] = cart_data(request)

    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}

    context['order'] = cart_data(request)

    return render(request, 'store/checkout.html', context)


def update_cart(request):
    # Converte-se a string em formato json recebido para um dicionário usando .loads
    data = json.loads(request.body)
    # print(data)

    # Coloca-se os dados recebidos dentro de variáveis
    action = data['action']
    product_id = data['product_id']
    size_id = data['size_id']
    color_id = data['color_id']

    # Recupera-se o customer
    customer = request.user.customer

    # Tenta recupera uma Order do Customer recuperado, sendo que essa Order deve ter on_cart True
    order, created = Order.objects.get_or_create(
        customer=customer, on_cart=True)

    # Recupera-se Product
    product = Product.objects.get(id=product_id)

    # Cria, ou recupera um item de Order, baseando-se nos dados enviados para o backend
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, price=product.price,
                                                          size_id=size_id,
                                                          color_id=color_id)

    # Dependendo do valor de action, faz uma ação diferente
    # -- add: adiciona ----  remove: reduz a quantidade em um ou exclui o item
    color = get_object_or_404(Color, id=color_id)
    if action == 'add':
        # Verifica-se a quantidade do produto disponível, e caso ainda exista uma quantidade disponível permite add
        if (order_item.quantity + 1) <= color.quantity:
            order_item.quantity += 1
            order_item.save()
            # print('added 1')

        else:
            return JsonResponse(
                {
                    'error_msg': f'The "{order_item.product.name}", in the size "{order_item.size.name}" and color "{order_item.color.name}" does not have the quantity of {order_item.quantity + 1} just {order_item.quantity}!'},
                safe=False, status=200)
    elif action == 'remove':
        # Se o usuário tentar remover uma unidade, verifica-se a quantidade, se o valor
        # for igual a 0 deleta o produto do cart
        if (order_item.quantity - 1) >= 1:
            order_item.quantity -= 1
            # print('removed 1')
            order_item.save()

        elif (order_item.quantity - 1) == 0:
            print(order_item.quantity)
            order_item.delete()
            print('product was deleted')

    return JsonResponse(
        {'message': "Cart was updated!", 'quantity_of_items': order.quantity_items},
        safe=False)


def process_order(request):
    user = request.user

    if user.is_authenticated:
        order = Order.objects.get(on_cart=True, customer=user.customer)
        order.on_cart = False
        order.status = 'PP'
        order.save()
        return JsonResponse('Order Was Completed!', safe=False,)

    else:
        ...
