document.querySelector('.overlay').style.display = "none";
document.querySelector('.modal__close').addEventListener('click', () => {
    document.querySelector('.overlay').style.display = "none";
})
document.querySelectorAll('.btn').forEach(item => {
    item.addEventListener('click', (event) => {
        event.preventDefault()
        document.querySelector('.overlay').style.display = "flex";
    })
})

const name__product = document.querySelector('#name__product'),
    select_category = document.querySelector('#select_category'),
    modal__submit = document.querySelector('.modal__submit input')
    select_region = document.querySelector('#select_region');

name__product.addEventListener('input', () => {
    fetch('/find_product/', {
        method: 'POST',
        body: JSON.stringify({
            'region': select_region.value,
            'category':select_category.value,
            'product': name__product.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            if (jsonResponse['found'] === false){
                modal__submit.style.cursor = 'not-allowed'
                modal__submit.disabled = true;
            }else {
                modal__submit.style.cursor = 'pointer'
                modal__submit.disabled = false;
            }
        })
})