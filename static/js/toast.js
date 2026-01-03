document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".toast");

    toasts.forEach(toast => {
        setTimeout(() => {
            toast.remove();
        }, 4200);
    });
});
