function initToasts() {
            const toasts = document.querySelectorAll('.toast');
            toasts.forEach(toast => {
                if (!toast.classList.contains('toast-initialized')) {
                    const bsToast = new bootstrap.Toast(toast, {
                        animation: false,
                        autohide: true,
                        delay: 3000
                    });
                    toast.classList.add('toast-initialized');
                    bsToast.show();
                }
            });
        }

document.addEventListener('DOMContentLoaded', function() {
    initToasts();
});