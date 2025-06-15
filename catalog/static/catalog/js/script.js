// Функция для обработки кнопок +/-
function handlePlusClick() {
  const input = this.closest(".quantity-selector, .input-group").querySelector(
    ".quantity-input"
  );
  input.value = parseInt(input.value) + 1;
}

function handleMinusClick() {
  const input = this.closest(".quantity-selector, .input-group").querySelector(
    ".quantity-input"
  );
  if (parseInt(input.value) > 1) {
    input.value = parseInt(input.value) - 1;
  }
}

// Функция для обработки отправки формы
function handleFormSubmit(e) {
  e.preventDefault(); // Предотвращаем стандартную отправку формы
  const form = this;
  const submitButton = form.querySelector('button[type="submit"]');

  // Сохраняем текущую позицию скролла
  const scrollPosition = window.scrollY || window.pageYOffset;
  sessionStorage.setItem("scrollPosition", scrollPosition);

  // Отключаем кнопку для предотвращения повторных отправок
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Добавляем...';
  }

  // Создаем скрытый input для сохранения позиции скролла
  let scrollInput = form.querySelector('input[name="scroll_position"]');
  if (!scrollInput) {
    scrollInput = document.createElement("input");
    scrollInput.type = "hidden";
    scrollInput.name = "scroll_position";
    form.appendChild(scrollInput);
  }
  scrollInput.value = scrollPosition;

  // Отправляем форму
  setTimeout(() => {
    form.submit();
  }, 0);
}

// Восстановление позиции скролла после загрузки страницы
function restoreScrollPosition() {
  const savedPosition = sessionStorage.getItem("scrollPosition");
  if (savedPosition !== null) {
    window.scrollTo({
      top: parseInt(savedPosition),
      behavior: "instant",
    });
    sessionStorage.removeItem("scrollPosition");
  }
}

// Инициализация действий корзины
function initCartActions() {
  // Обработчики для кнопок +/-
  document.querySelectorAll(".plus-btn").forEach((btn) => {
    btn.removeEventListener("click", handlePlusClick);
    btn.addEventListener("click", handlePlusClick);
  });

  document.querySelectorAll(".minus-btn").forEach((btn) => {
    btn.removeEventListener("click", handleMinusClick);
    btn.addEventListener("click", handleMinusClick);
  });

  // Обработчик отправки формы
  document.querySelectorAll(".add-to-cart-form").forEach((form) => {
    form.removeEventListener("submit", handleFormSubmit);
    form.addEventListener("submit", handleFormSubmit);
  });
}

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
  initCartActions();
  restoreScrollPosition();
});
