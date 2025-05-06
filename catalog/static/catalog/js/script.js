// Функция для обработки кнопок +/-
function handlePlusClick() {
    const input = this.closest('.input-group').querySelector('.quantity-input');
    input.value = parseInt(input.value) + 1;
}

function handleMinusClick() {
    const input = this.closest('.input-group').querySelector('.quantity-input');
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
    }
}

// Функция для обработки отправки формы
function handleFormSubmit(e) {
    e.preventDefault(); // Предотвращаем стандартную отправку формы
    const form = this;
    const submitButton = form.querySelector('button[type="submit"]');

    // Отключаем кнопку для предотвращения повторных отправок
    if (submitButton) {
        submitButton.disabled = true;
    }

    // Сохраняем позицию скролла
    const scrollPosition = window.scrollY || window.pageYOffset;
    localStorage.setItem('scrollPosition', scrollPosition);

    // Отправляем форму
    setTimeout(() => {
        form.submit();
    }, 0);
}

// Инициализация действий корзины
function initCartActions() {
    // Обработчики для кнопок +/-
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.removeEventListener('click', handlePlusClick); // Удаляем старый обработчик
        btn.addEventListener('click', handlePlusClick);
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.removeEventListener('click', handleMinusClick);
        btn.addEventListener('click', handleMinusClick);
    });

    // Обработчик отправки формы
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.removeEventListener('submit', handleFormSubmit);
        form.addEventListener('submit', handleFormSubmit);
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Восстанавливаем позицию скролла
    const savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition !== null) {
        window.scrollTo({
            top: parseInt(savedScrollPosition),
            behavior: 'instant'
        });
        localStorage.removeItem('scrollPosition');
    }

    // Инициализация действий корзины
    initCartActions();
});