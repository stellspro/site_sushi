
let cart = {};
let order = {}
let myModal = new bootstrap.Modal(document.getElementById('exampleModal'),{
    keboard: false
})




$.getJSON('/get-pizza', function(data) {
    let goods = data;
    // console.log(goods);
    checkCart();
    showCart();

    function showCart(){
        if ($.isEmptyObject(cart)) {
            out = 'Корзина пуста. Добавьте товар в корзину. <a href="/">Главная страница</>';
            $('#cart').html(out);
        }
        else{
            let out = "";
            let summ = 0;        
            for (let key in cart){    
                out+=`<div class="col-xl-12 col-md-6 col-sm-12" style="display: flex; align-self: stretch;">`
                out+=`<div class="card " style="width: 15rem; margin-bottom: 20px; margin-top: 20px; background-color:#dad6d6c7;">`
                out+=`<img src="/static/img/${goods[key].image}" alt="">`
                out+=`<div class="card-body" style="display: flex flex-direction: column justify-content: space-between;">`
                out+=`<div>`
                out+=`<h4>${goods[key].name} </h4>`
                out+='<br>'
                // out+=`<h4>Цена: ${goods[key].price}</h4>`
                out+='<br>'
                out+=`<h4>Количество:${cart[key]}</h4>`
                out+='<br>'
                out+=`</div>`
                out+= '<button class="delete" data-art="'+key+'">Удалить из корзины</button>';
                // out+= goods[key].coast + 'руб';  
                out+= '<button class="minus" data-art="'+key+'">-</button>';
                // out+= cart[key];   
                out+= '<button class="plus" data-art="'+key+'">+</button>';
                out+= cart[key]*goods[key].price + 'руб';
                out+= '<br>'
                out+=`</div>`
                out+=`</div>`
                out+=`</div>`
                summ+= cart[key]*goods[key].price;
            }
            out+= '<p> Всего:  '+summ+' рублей</p>';
        
            out+= '<button class="add btn-success" type="button" data-bs-toggle="modal" data-bs-target="#exampleModal">Заказать </button>'
            // out+=`</div>`
            $('#cart').html(out);
            $('.plus').on('click', plusGoods)
            $('.minus').on('click', minusGoods)
            $('.delete').on('click', deleteGoods)
            // $('.order').on('click', takeCart)
            // $('.order').on('click', checkout)
            }
        
    }

    function plusGoods(){
        let articul = $(this).attr('data-art');
        cart[articul]++;
        saveGoodsToLS();
        showCart();
    }

    function minusGoods(){
        let articul = $(this).attr('data-art');
        if (cart[articul] >1) cart[articul]--;
        else delete cart[articul];
        saveGoodsToLS();
        showCart();
        
    }

    function deleteGoods(){
        let articul = $(this).attr('data-art');
        delete cart[articul];
        saveGoodsToLS();
        showCart();
    }
    function takeCart() {
        let products_id = []
        let products_coast = []
        console.log(cart)
        for(let key in cart){
            products_id.push(goods[key]['id'])
            products_coast.push(cart[key])

        }
        console.log(products_id)
        console.log(products_coast)
        console.log(order['name'])
        console.log(order)
        $.ajax({
            type: "POST",
            url: '/order_page',
            data: JSON.stringify({ 'id': products_id , 'coast': products_coast, 'user_name' : order['name'], 'phone': order['phone'], 'address':order['address'], 'payment':'наличные' }),
            contentType : "application/json"
          })
        cart = {}
        saveGoodsToLS()
        showCart()
    }
    
   
    
    document.querySelector('button.add_new').addEventListener('click', function(e) {    
    let user_name = document.getElementById('name_user').value
    let phone = document.getElementById('user_phone').value
    let address = document.getElementById('address').value
    order['name'] = user_name
    order['phone'] = phone
    order['address'] = address
    if (user_name && phone && address) {
        document.getElementById('name_user').value = ''
        document.getElementById('user_phone').value = ''
        document.getElementById('address').value = ''
        myModal.hide() 
        console.log(user_name)
        console.log(phone)
        console.log(address)
        takeCart()       
    } else {
            Swal.fire({
                icon: 'error',
                title: 'Ошибка',
                text: 'Пожалуйста заполните все поля!',
            })

            }
            
            
        })  
});



function checkCart() {
    // проверяем наличие корзины в localstorage
    if  (localStorage.getItem('cart') != null) {
        cart = JSON.parse(localStorage.getItem('cart'));
    }
}

function saveGoodsToLS(){
    localStorage.setItem('cart', JSON.stringify(cart));
}