const counters = document.querySelectorAll('.name-counter-price-wrapper');
const totalBasketPrice = document.querySelector('.basket-total-price span');
let totalPrice = 0;

counters.forEach((element, index) => {
    const counterNumber = element.querySelector('.basket-counter-number');
    const counterBtn = element.querySelectorAll('.basket-counter-button');
    const productPrice = element.querySelector('.basket-item-price span');
    var price = Number(productPrice.innerHTML.replace(/ /g,''));
    let counter = 1;
    let newPrice = 0;

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
            counterNumber.textContent = counter;
            productPrice.textContent = newPrice;
            setDisabled(counter, counterBtn);
            setPrice(totalPrice);
        });
    });
    totalPrice += price;
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
