const form = document.querySelector("form");
const button = form.querySelector("button");

form.addEventListener("submit", () => {
    button.disabled = true;
    button.classList.add("loading");

    const text = button.querySelector(".btn-text");
    if (text) text.textContent = "Entrando...";
});
