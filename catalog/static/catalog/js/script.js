function initCartActions() {
    // Обработчики для кнопок +/-
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.closest('.input-group').querySelector('.quantity-input');
            input.value = parseInt(input.value) + 1;
        });
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.closest('.input-group').querySelector('.quantity-input');
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });

    // Обработчик отправки формы
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Предотвращаем стандартную отправку
            
            // Показываем уведомление
            const quantity = this.querySelector('.quantity-input').value;
            alert(`Товар добавлен в корзину (количество: ${quantity})`);
            
            // Отправляем форму
            this.submit();
        });
    });
}

document.addEventListener('DOMContentLoaded', initCartActions);