document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const username = form?.querySelector("input[name='username']");
    const password = form?.querySelector("input[name='password']");
    const submitBtn = form?.querySelector("button[type='submit']");

    if (!form || !username || !password || !submitBtn) return;

    function showError(input, message) {
        input.classList.add("input-error");

        let error = input.parentElement.querySelector(".field-error");
        if (!error) {
            error = document.createElement("div");
            error.className = "field-error";
            input.parentElement.appendChild(error);
        }

        error.textContent = message;
    }

    function clearError(input) {
        input.classList.remove("input-error");
        const error = input.parentElement.querySelector(".field-error");
        if (error) error.remove();
    }

    function validate() {
        let valid = true;

        if (username.value.trim().length < 3) {
            showError(username, "Usuário precisa ter pelo menos 3 caracteres");
            valid = false;
        } else {
            clearError(username);
        }

        if (password.value.trim().length < 4) {
            showError(password, "Senha precisa ter pelo menos 4 caracteres");
            valid = false;
        } else {
            clearError(password);
        }

        submitBtn.disabled = !valid;
        submitBtn.style.opacity = valid ? "1" : "0.6";

        return valid;
    }

    username.addEventListener("input", validate);
    password.addEventListener("input", validate);

    form.addEventListener("submit", e => {
        if (!validate()) e.preventDefault();
    });

    validate();


    // 🧩 PASSO 8.3 — MEDIDOR DE FORÇA DA SENHA
    const strengthBar = document.getElementById("strengthBar");
    const strengthText = document.getElementById("strengthText");

    if (password && strengthBar && strengthText) {
        password.addEventListener("input", () => {
            const value = password.value;

            strengthBar.className = "strength-bar";

            if (value.length < 4) {
                strengthBar.classList.add("strength-weak");
                strengthText.textContent = "Senha fraca";
            } 
            else if (value.length < 8) {
                strengthBar.classList.add("strength-medium");
                strengthText.textContent = "Senha média";
            } 
            else {
                strengthBar.classList.add("strength-strong");
                strengthText.textContent = "Senha forte";
            }
        });
    }

});
