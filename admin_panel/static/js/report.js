// Функция для увеличения количества в категории
function increaseQuantity(category) {
    // Получаем элемент span, который отображает текущее количество
    const displaySpan = document.getElementById(category + '_display');
    // Получаем скрытый input, который хранит текущее количество
    const hiddenInput = document.getElementById(category + '_input');
    // Преобразуем текстовое содержимое span в целое число
    const currentValue = parseInt(displaySpan.textContent);
    // Увеличиваем значение на 1 и обновляем span и input
    displaySpan.textContent = currentValue + 1;
    hiddenInput.value = currentValue + 1;
}

// Функция для уменьшения количества в категории
function decreaseQuantity(category) {
    // Получаем элемент span, который отображает текущее количество
    const displaySpan = document.getElementById(category + '_display');
    // Получаем скрытый input, который хранит текущее количество
    const hiddenInput = document.getElementById(category + '_input');
    // Преобразуем текстовое содержимое span в целое число
    const currentValue = parseInt(displaySpan.textContent);
    // Проверяем, что текущее значение больше 0, чтобы не было отрицательных значений
    if (currentValue > 0) {
        // Уменьшаем значение на 1 и обновляем span и input
        displaySpan.textContent = currentValue - 1;
        hiddenInput.value = currentValue - 1;
    }
}