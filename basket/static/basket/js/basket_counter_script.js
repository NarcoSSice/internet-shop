const counters = document.querySelectorAll('.name-counter-price-wrapper');
const totalBasketPrice = document.querySelector('.basket-total-price span');
let totalPrice = 0;

counters.forEach((element, index) => {
    const counterNumber = element.querySelector('.basket-counter-number');
    const counterBtn = element.querySelectorAll('.basket-counter-button');
    const productPrice = element.querySelector('.basket-item-price span');
    const productId = Number(element.querySelector('.basket-product-item-id[hidden]').innerHTML);
    let fixedPrice = Number(productPrice.innerHTML.replace(/ /g,''));
    let counter = Number(counterNumber.innerHTML);
    var price = fixedPrice / counter;
    let newPrice = 0;

    setDisabled(counter, counterBtn);
    counterBtn.forEach((el, index) => {
        el.addEventListener('click', () => {
            if (index === 0 && counter > 1) {
                counter--;
                totalPrice -= price;
            } else if (index === 1 && counter < 5) {
                counter++;
                totalPrice += price;
            }
            newPrice = counter * price;
            updateProductQuantity(productId, counter);
            counterNumber.textContent = counter;
            productPrice.textContent = newPrice;
            setDisabled(counter, counterBtn);
            setPrice(totalPrice);
        });
    });
    totalPrice += fixedPrice;
    setPrice(totalPrice);
});

function setDisabled(counter, counterBtn) {
    if (counter === 1) {
        counterBtn[0].disabled = true;
    } else if (counter === 5) {
        counterBtn[1].disabled = true;
    } else {
        counterBtn[0].disabled = false;
        counterBtn[1].disabled = false;
    }
}

function setPrice(price) {
    totalBasketPrice.textContent = price;
}

const updateProductQuantity = (productId, newQuantity) => {
    fetch('/basket/update_quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            product_id: productId,
            new_quantity: newQuantity,
        }),
    })
    .then(response => {
        if (response.ok) {
            // Обработка успешного обновления
            console.log('Количество товара обновлено!');
        } else {
            // Обработка ошибки
            console.error('Ошибка при обновлении количества товара');
        }
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
};

const getCSRFToken = () => {
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    return csrfToken;
};
