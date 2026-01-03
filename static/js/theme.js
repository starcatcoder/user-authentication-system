document.addEventListener("DOMContentLoaded", () => {
    const themeBtn = document.querySelector(".theme-btn");
    if (!themeBtn) return;

    const body = document.body;

    // Define ícone correto ao carregar
    if (body.classList.contains("dark")) {
        themeBtn.textContent = "☀️";
    } else {
        themeBtn.textContent = "🌙";
    }

    themeBtn.addEventListener("click", () => {
        body.classList.toggle("dark");

        const isDark = body.classList.contains("dark");
        themeBtn.textContent = isDark ? "☀️" : "🌙";

        // Salva no backend
        fetch("/theme", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ theme: isDark ? "dark" : "light" })
        });
    });
});
