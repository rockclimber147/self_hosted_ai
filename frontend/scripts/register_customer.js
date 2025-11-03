const BACKEND_URL = "https://ai.daylensmith.ca";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('registrationForm');
    const registerBtn = document.getElementById('registerBtn');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const emailInput = document.getElementById('email');

    function showMessage(message, type) {
        const box = document.getElementById('messageBox');
        const text = document.getElementById('messageText');

        box.className = 'message-box p-3 rounded-lg text-sm show';

        if (type === 'success') {
            box.classList.add('bg-green-100', 'text-green-800');
            box.classList.remove('bg-red-100', 'text-red-800', 'hidden');
        } else if (type === 'error') {
            box.classList.add('bg-red-100', 'text-red-800');
            box.classList.remove('bg-green-100', 'text-green-800', 'hidden');
        } else {
            box.classList.add('bg-gray-100', 'text-gray-800');
            box.classList.remove('bg-red-100', 'text-red-800', 'hidden');
        }

        text.textContent = message;

        setTimeout(() => {
            box.classList.remove('show');
            setTimeout(() => box.classList.add('hidden'), 300);
        }, 5000);
    }
    
    function validateForm() {
        const passwordsMatch = passwordInput.value === confirmPasswordInput.value && passwordInput.value.length >= 8;
        const emailValid = emailInput.value.includes('@') && emailInput.value.length > 0;

        if (passwordsMatch && emailValid) {
            registerBtn.disabled = false;
            confirmPasswordInput.classList.remove('border-red-500');
        } else {
            registerBtn.disabled = true;
            if (confirmPasswordInput.value.length > 0 && passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.classList.add('border-red-500');
            } else {
                confirmPasswordInput.classList.remove('border-red-500');
            }
        }
    }

    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    confirmPasswordInput.addEventListener('input', validateForm);


    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (passwordInput.value !== confirmPasswordInput.value) {
            showMessage('Error: Passwords do not match.', 'error');
            confirmPasswordInput.focus();
            return;
        }
        
        registerBtn.disabled = true;
        registerBtn.textContent = 'Registering...';

        const registrationData = {
            email: emailInput.value,
            password: passwordInput.value,
        };

        const apiUrl = `${BACKEND_URL}/user/create`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(registrationData),
                credentials: 'include' 
            });

            if (response.ok) {
                const result = await response.json();
                showMessage(`Registration successful! You can now log in.`, 'success');
                
                setTimeout(() => {
                    window.location.href = "customer_login.html";
                }, 2000);

            } else if (response.status === 409) {
                showMessage('Error: This email address is already registered.', 'error');
            }
            else {
                const errorData = await response.json().catch(() => ({ message: 'Registration failed due to server error.' }));
                showMessage(`Error: ${errorData.message || 'Registration failed.'}`, 'error');
            }
        } catch (error) {
            showMessage('Network Error: Could not reach the server.', 'error');
            console.error('Registration fetch failed:', error);
        } finally {
            registerBtn.textContent = 'Register';
            validateForm();
        }
    });
});