function increaseQuantity(category, maxAmount) {
    // Получаем элемент span, который отображает текущее количество
    const displaySpan = document.getElementById(category + '_display');
    // Получаем скрытый input, который хранит текущее количество
    const hiddenInput = document.getElementById(category + '_input');
    // Преобразуем текстовое содержимое span в целое число
    const currentValue = parseInt(displaySpan.textContent);
    // Проверяем, что текущее значение меньше или равно maxAmount
    if (currentValue < maxAmount) {
        // Увеличиваем значение на 1 и обновляем span и input
        displaySpan.textContent = currentValue + 1;
        hiddenInput.value = currentValue + 1;
    }
}

function decreaseQuantity(category, maxAmount) {
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

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('report-form');
    const alertMessage = document.getElementById('alert-message');

    form.addEventListener('submit', (event) => {
        const inputs = document.querySelectorAll('input[type="hidden"][id^="feed_"]');
        let allZero = true;
        inputs.forEach(input => {
            if (parseInt(input.value) > 0) {
                allZero = false;
            }
        });

        if (allZero) {
            alertMessage.style.display = 'block';
            event.preventDefault();
        } else {
            alertMessage.style.display = 'none';
        }
    });
});
