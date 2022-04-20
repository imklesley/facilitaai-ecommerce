let update_cart_btns = document.getElementsByClassName('update-cart')

for (let i = 0; i < update_cart_btns.length; i++) {

    update_cart_btns[i].addEventListener('click', function () {

        let action = this.dataset.action
        let product_id = this.dataset.product
        let size_id = this.dataset.size
        let color_id = this.dataset.color
        // console.log(action, product_id, size_id, color_id)


        if (size_id === undefined || color_id === undefined) {
            try {
                //TODO: Mensagem de erro obrigando adicionar a medida ou a cor da peça
                size_id = document.querySelector("input[name=product" + product_id + "-size-option]:checked").value
                color_id = document.querySelector("input[name=product" + product_id + "-color-option]:checked").value

                console.log('Action:', action, "\nProduct:", product_id, '\nSize:', size_id, '\nColor:', color_id)

                if (is_user_authenticated) {
                    console.log('User is logged in, lets send the data to database')
                    update_cart(action, product_id, size_id, color_id)

                } else {
                    console.log('User not logged in, lets save the user data on browser cookies')
                    update_cookie_cart(action, product_id, size_id, color_id)
                    console.log(cart)
                }

                // Hide color after "add to cart"
                let size_colors = document.getElementsByClassName('size-colors')

                for (let j = 0; j < size_colors.length; j++) {
                    size_colors[j].classList.add('hidden')
                }
                //


                // Unchecked all groups of radio buttons
                $('.btn-group :radio').prop('checked', false);
                $('.btn-group .active').removeClass('active');
                //

                // If the user has the error message on the screen, but he has already added size and color, and added to the cart
                // will make the error message disappear
                let product_alert = document.getElementById('alert-product-' + product_id)
                product_alert.style.display = 'none'


            } catch
            (e) {
                console.error(e)
                let product_alert = document.getElementById('alert-product-' + product_id)
                product_alert.style.display = 'block'
                setTimeout(function () {
                    product_alert.style.display = 'none'
                }, 5000)
            }
        } else {
            if (is_user_authenticated) {
                console.log('User is logged in, lets send the data to database')
                update_cart(action, product_id, size_id, color_id)
                location.reload()

            } else {
                console.log('User not logged in, lets save the user data on browser cookies')
                update_cookie_cart(action, product_id, size_id, color_id)
                location.reload()
            }
        }
    }
    )


    function update_cart(action, product_id, size_id, color_id) {
        const URL = '/update_cart/'

        fetch(URL, {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                'X-CSRFToken': csrf_token
            },
            "body": JSON.stringify({
                'action': action,
                'product_id': product_id,
                'size_id': size_id,
                'color_id': color_id,
            }),
        }
        ).then(async (response) => {
            if (response.status === 200) {
                let data = await response.json();

                if (data['error_msg']) {
                    let error_element = document.getElementById('failed-add-product-to-cart-' + product_id)
                    error_element.innerText = data['error_msg']
                    error_element.classList.remove('hidden')
                    setTimeout(() => {
                        error_element.classList.add('hidden')
                    }, 8000);
                } else {
                    let success_element = document.getElementById('succeed-add-product-to-cart-' + product_id)
                    success_element.innerText = 'The product has been added to the cart!'
                    success_element.classList.remove('hidden')
                    setTimeout(() => {
                        success_element.classList.add('hidden')
                    }, 3500);
                }

                return data
            }

        }).then((data) => {
            // console.log(data)
            if (data['quantity_of_items']) {
                let quantity_element = document.getElementById('quantity_of_items')
                quantity_element.innerText = data['quantity_of_items']
            }
        })
    }




    function update_cookie_cart(action, product_id, size_id, color_id) {
        let quantity_element = document.getElementById('quantity_of_items')
        // Caso seja a ação de adicionar ao carrinho, verifica seo item já existe no dict cart, caso exista
        // adicione o valor +1 a quantity, caso contrário adicione um dict a chave product_id com todos os 
        // atributos do produto que está sendo adicionado(size e color)
        let product = `${product_id}-${size_id}-${color_id}`

        if (action === 'add') {
            if (product in cart) {
                cart[product]['quantity'] += 1
            }
            else {
                cart[product] = { 'product_id': product_id, 'size_id': size_id, 'color_id': color_id, 'quantity': 1 }
            }

            quantity_element.innerText = (+quantity_element.innerText) + 1
            //console.log(quantity_element.innerText)

        }
        // Caso seja remoção retire uma unidade da quantidade do produto QUE ESTÀ no cart, caso o valor
        // após a remoção for 0, retira o produto do cart
        else if (action === 'remove') {
            if (product in cart) {
                cart[product]['quantity'] -= 1
                if (cart[product]['quantity'] <= 0) {
                    delete cart[product]
                }
                quantity_element.innerText = (+quantity_element.innerText) - 1

            }
        }


        // Salva as alterações no cookie
        document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/;`

    }


}













