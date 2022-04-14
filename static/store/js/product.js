let product_sizes = document.getElementsByClassName('product-size')

for (let i = 0; i < product_sizes.length; i++) {
    product_sizes[i].addEventListener('click', () => {
        let size_id = product_sizes[i].id

        let colors_id = size_id.replace('product-size', 'size-colors')

        let size_colors = document.getElementById(colors_id)

        let groups_size_colors = document.getElementsByClassName('size-colors')

        for (let j = 0; j < groups_size_colors.length; j++) {
            groups_size_colors[j].classList.add('hidden')
        }

        size_colors.classList.remove('hidden')
        
    })
}


