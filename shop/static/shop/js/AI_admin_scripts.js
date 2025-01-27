async function uploadImageFromAI(imageUrl) {
    const inputFile = document.querySelector('#id_image');

    // Завантажуємо файл з imageUrl
    const response = await fetch(imageUrl); // URL, який повертає ШІ
    console.log(response)
    const blob = await response.blob(); // Створюємо Blob з отриманих даних

    // Створюємо об'єкт File, щоб додати його до input
    const file = new File([blob], 'generated_image.jpg', { type: blob.type });

    // Оновлюємо поле файлу через DataTransfer API
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    inputFile.files = dataTransfer.files;

    console.log('Файл успішно додано до input!');
}


(function($) {
    $(document).ready(function() {
        // Додаємо кнопку біля поля description
        const generateDescriptionButton = $('<button type="button" class="button" id="generate-description">Згенерувати опис</button>');
        const generatePriceButton = $('<button type="button" class="button" id="generate-price">Надати ринкову ціну</button>');
        const generateImageButton = $('<button type="button" class="button" id="generate-image">Згенерувати фото</button>');
        const viewImageButton = $('<a class="button" id="view-image" href="#" target="_blank" style="display: none;">Переглянути фото</a>');
        generateDescriptionButton.insertAfter('#id_description');
        generatePriceButton.insertAfter('#id_price');
        generateImageButton.insertAfter('#id_image');
        viewImageButton.insertAfter('#generate-image');

        let generatedImageUrl = '';

        // Обробка натискання кнопки
        $('#generate-description').click(function() {
            const productName = $('#id_name').val();  // Отримуємо назву товару
            const subcategory = $('#id_subcategory').val();  // Отримуємо категорію

            if (productName && subcategory) {
                // Відправляємо запит на сервер для генерації опису
                $.ajax({
                    url: '/admin/generate_description/',  // URL для обробки запиту
                    data: {
                        'product_name': productName,
                        'subcategory': subcategory
                    },
                    success: function(response) {
                        $('#id_description').val(response.description);  // Вставляємо згенерований опис у поле
                    },
                    error: function() {
                        alert('Помилка при генерації опису');
                    }
                });
            } else {
                alert('Будь ласка, введіть назву товару та виберіть категорію');
            }
        });

        $('#generate-price').click(function() {
            const productName = $('#id_name').val();  // Отримуємо назву товару
            const subcategory = $('#id_subcategory').val();  // Отримуємо категорію

            if (productName && subcategory) {
                // Відправляємо запит на сервер для генерації опису
                $.ajax({
                    url: '/admin/generate_price/',  // URL для обробки запиту
                    data: {
                        'product_name': productName,
                        'subcategory': subcategory
                    },
                    success: function(response) {
                        $('#id_price').val(response.price);  // Вставляємо згенерований опис у поле
                    },
                    error: function() {
                        alert('Помилка при генерації ціни');
                    }
                });
            } else {
                alert('Будь ласка, введіть назву товару та виберіть категорію');
            }
        });

        $('#generate-image').click(function() {
            const productName = $('#id_name').val();  // Отримуємо назву товару
            const subcategory = $('#id_subcategory').val();  // Отримуємо категорію

            if (productName && subcategory) {
                // Відправляємо запит на сервер для генерації опису
                $.ajax({
                    url: '/admin/generate_image/',  // URL для обробки запиту
                    data: {
                        'product_name': productName,
                        'subcategory': subcategory
                    },
                    success: async function(response) {
                        try {
                            const imageUrl = response.imageUrl;
                            await uploadImageFromAI(imageUrl);
                             $('#view-image').attr('href', imageUrl).show();
                        } catch (error) {
                            alert('Помилка завантаження картинки');
                        }
                    },
                    error: function() {
                        alert('Помилка при генерації картинки');
                    }
                });
            } else {
                alert('Будь ласка, введіть назву товару та виберіть категорію');
            }
        });
    });
})(django.jQuery);

