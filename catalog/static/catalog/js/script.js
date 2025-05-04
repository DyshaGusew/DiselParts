function initCartActions() {

    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.id;
            const input = document.querySelector(`.quantity-input[data-id="${productId}"]`);
            input.value = parseInt(input.value) + 1;
        });
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.id;
            const input = document.querySelector(`.quantity-input[data-id="${productId}"]`);
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });
    
    document.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.id;
            const quantity = document.querySelector(`.quantity-input[data-id="${productId}"]`).value;
            alert('Товар '+ productId +' (количество: ' + quantity + ') добавлен в корзину!');
        });
    });
}

// Инициализация при загрузке документа
document.addEventListener('DOMContentLoaded', initCartActions);