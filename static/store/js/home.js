// Efeito de sombra nos cards ao posicionar mouse sobre cards
const card_products = document.getElementsByClassName('card-product')

for (let key in card_products) {

    const card = card_products[key]
    card.addEventListener('mouseover', () => {
        card.classList.remove('shadow-sm')
        card.classList.add('shadow-lg')
    })

    card.addEventListener('mouseout', () => {
        card.classList.remove('shadow-lg')
        card.classList.add('shadow-sm')
    })
}



/////////


