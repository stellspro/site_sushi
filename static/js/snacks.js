let cart = {}
$(document).ready(function(){
    loadGoods()
    checkCart()
    showMiniCart()
})


function loadGoods(){
    $.post('/get-snacks', function (data) {
        // получение списка продуктов по категории
        data = JSON.parse(data)
        console.log(data)
        //вывод продуктов на странице
        let goods = ``
        for (let i in data){
            goods+=`<div class="col-xl-3 col-md-6 col-sm-12" style="display: flex; align-self: stretch;">`
            goods+=`<div class="card " style="width: 15rem; margin-bottom: 20px; margin-top: 20px; background-color:#dad6d6c7;">`
            goods+=`<img src="/static/img/${data[i]['image']}" class="img-thumbnail" alt="...">`
            goods+=`<div class="card-body" style="display: flex flex-direction: column justify-content: space-between;">`
            goods+=`<div>`
            goods+=` <h4 class="card-title"><strong>${data[i]['name']}</strong></h4>`
            goods+=`<br>`
            goods+=`<h5 class="card-title" style="color:chocolate;">${data[i]['price']} р.</h5>`
            goods+=`<br>`
            goods+=`<p class="card-text"><em>${data[i]['description']}</em></p>`
            goods+=`<br>`
            goods+=`</div>`
            goods+=`<button class="add_cart btn btn-outline-dark" data-art="${i}">Заказать</button>`
            goods+=`</div>`
            goods+=`</div>`
            goods+=`</div>`
        }
        $('#pizza').html(goods);
        $('button.add_cart').on('click', addToCart)
        console.log(data[1]['price'])
        // document.querySelector('.total-price').innerHTML = data[1]['price']
    });
}

function addToCart() {
    // добавление продукта в корзину
    let articul = $(this).attr('data-art')
    if (cart[articul] != undefined) {
        cart[articul]++;
    }
    else {
       cart[articul] = 1
    }
    localStorage.setItem('cart', JSON.stringify(cart))
    // console.log(cart);
    showMiniCart()
}

function checkCart() {
    // проверка наличия корзины в localstorage
    if  (localStorage.getItem('cart') != null) {
        cart = JSON.parse(localStorage.getItem('cart'));
    }
}

function showMiniCart() {
    $.post('/get-products', function (data) {
    //вывод содержимого мини корзины
    data = JSON.parse(data)
    let goods = data
    let out = ''
    for (let w in cart) {
        out += goods[w].name + '---' +cart[w]+ '<br>'
        $('#mini-cart').html(out)
    }
})
}