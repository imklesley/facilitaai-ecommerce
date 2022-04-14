let update_cart_btns = document.getElementsByClassName('update-cart')

for (let i = 0; i < update_cart_btns.length; i++) {

    update_cart_btns[i].addEventListener('click', function () {

        let action = this.dataset.action
        let product_id = this.dataset.product

        try {
            //TODO: Mensagem de erro obrigando adicionar a medida ou a cor da peça
            let size_id = document.querySelector("input[name=product" + product_id + "-size-option]:checked").value
            let color_id = document.querySelector("input[name=product" + product_id + "-color-option]:checked").value
            console.log('Action:', action, "\nProduct:", product_id, '\nSize:', size_id, '\nColor:', color_id)



           console.log('saasads')


            if (is_user_authenticated) {
                console.log('User is logged in, lets send the data to database')

            } else {
                console.log('User not logged in')
            }





        } catch (e) {
            let product_alert = document.getElementById('alert-product-' + product_id)
            product_alert.style.display = 'block'
            setTimeout(function () {
                product_alert.style.display = 'none'
            }, 5000)
        }
    })

}











