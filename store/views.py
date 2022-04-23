from django.shortcuts import redirect, render
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


def process_order_whatsapp(request):
    # nº da loja que irá receber o pedido
    whatsapp_number = '5563999500153'

    user = request.user

    if user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=user.customer,on_cart=True)
        # Caso o usuário fazer o pedido pelo wttps diretamente pela url
        if created or order.orderitem_set.count() == 0 :
            return redirect('/')
       

        whatsapp_order_text = order.whatsapp_order_text
        # print(order.whatsapp_order_text)

    else:
        user_data = json.loads(request.body).get('user_data')
        user_address = json.loads(request.body).get('user_address')
        # print(user_data)
        # print(user_address)

        #Transforma cookie em order
        order = cart_data(request)

        # Código para pular linha
        break_line = '%0A'
        # pego todos os itens dentro do pedido
        items = order['orderitem_set']['all']
        # Inicializo o texto a ser enviado pro cliente e adiciono duas vezes o break_line
        whatsapp_order_text = f'Olá, gostaria de realizar o pedido: {break_line}{break_line}'
        
        # Pra cada item da ordem especificar os detalhes e pular uma linha
        for item in items:
            whatsapp_order_text += f"*{item['quantity']}x*\t-\t{item['product'].name}\t-\t{item['size'].name}\t-\t{item['color'].name}\t- R$ \t{item['product'].price}{break_line}"

        whatsapp_order_text += break_line
        whatsapp_order_text += '-----------------------------' + break_line

        # Mostra os quantitativos
        whatsapp_order_text += f"*Quantidade de Itens:* {order['quantity_items']}{break_line}"
        whatsapp_order_text += f"*Total:* R$ {order['total_price']}{break_line}{break_line}"


         # Dados do customer
        whatsapp_order_text += '------------ Dados do Cliente -----------' + break_line
        whatsapp_order_text += f'*Nome:* {user_data["name"]}{break_line}'
        whatsapp_order_text += f'*Email:* {user_data["email"]}{break_line}{break_line}'
        whatsapp_order_text += f'*Cidade-UF:* {user_address["city"]}-{user_address["state"]}{break_line}'
        whatsapp_order_text += f'*Endereço:* {user_address["address"]}{break_line}'
        whatsapp_order_text += f'*CEP:* {user_address["zipcode"]}{break_line}'

        


    whatsapp_url_with_data = f'https://api.whatsapp.com/send/?phone={whatsapp_number}&text={whatsapp_order_text}&app_absent=0'

    return JsonResponse(whatsapp_url_with_data,safe=False)