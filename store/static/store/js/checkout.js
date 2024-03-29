// Faz a caixa com informações de endereço invisível
let payment_data = document.getElementById("payment-data")
if (is_user_authenticated) {
    payment_data.classList.remove('hidden')
}


// Caso o usuário não esteja autenticado, vai fazer o botão de continuar desaparecer e fará aparcer o card de pagamento
if (!is_user_authenticated) {
    let form = document.getElementById('checkout-form')

    form.addEventListener('submit', (event) => {
        event.preventDefault()
        // console.log('Submitedd')

        document.getElementById("btn-checkout-submit").classList.add('hidden')
        document.getElementById("payment-data").classList.remove('hidden')

    })
}


// Ações de cada botão

let make_payment = document.getElementById('make-payment')
make_payment.addEventListener('click', function (event) {
    console.log('Let\'s pay!')

    const url = '/process_order/'

    fetch(url, {
        "method": "POST",
        "headers": {
            'X-CSRFToken': csrf_token
        }
    }).then(function (response) {

        if (response.status == 200) {
            return response.json()
        }
    }).then((data) => {
        // console.log(data)
        alert('Your order was completed, your payment is processing now!!')

        // Limpa o cookie cart
        if (!is_user_authenticated) {
            document.cookie = "cart={};domain=;path=/"
        }


        //Retorna para a página inicial
        location.href = "/"
    })

})


let continue_on_whatsapp = document.getElementById('continue-on-whatsapp')
continue_on_whatsapp.addEventListener('click', () => {
    console.log('Let\'s continue on whatspp!')

    let user_data = {}
    let user_address = {}

    if (!is_user_authenticated) {
        const form = document.getElementById('checkout-form')

        user_data = { "name": form['name'].value, "email": form['email'].value }
        
        user_address = { "address": form['address'].value, "city": form['city'].value, "state": form['state'].value, "zipcode": form['zipcode'].value }
        
    }


    const url = '/process_order_whatsapp/'
    fetch(url, {
        "method": "POST",
        "headers": {
            "X-CSRFToken": csrf_token
        },
        "body":JSON.stringify({"user_data":user_data,"user_address":user_address})
    }).then((response) => {
        if (response.status === 200) {
            return response.json()
        }
    }).then((data) => {
        //console.log(data)
        location.href = data
    })






})






