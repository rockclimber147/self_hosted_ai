import BACKEND_URL from "./config";

const showMessage = (message, type) => {
    const msgBox = document.getElementById('message-box');
    let color, background;
    if (type === 'success') {
        color = 'text-green-800';
        background = 'bg-green-100';
    } else if (type === 'error') {
        color = 'text-red-800';
        background = 'bg-red-100';
    }

    msgBox.className = `p-3 mb-4 rounded-lg text-sm transition-all duration-300 ${color} ${background}`;
    msgBox.textContent = message;
    msgBox.classList.remove('hidden');

    setTimeout(() => {
        msgBox.classList.add('hidden');
    }, 5000);
};

document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const apiUrl = `${BACKEND_URL}/user/login`;

    if (!email || !password) {
        showMessage('Please enter both email and password.', 'error');
        return;
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (response.ok) {
            showMessage('Login successful! Redirecting...', 'success');
            
            setTimeout(() => {
                window.location.href = 'customer_landing.html'; 
            }, 1000); 

        } else {
            let errorDetail = `Login failed. Status: ${response.status}.`;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || `Server status: ${response.status}`; 
            } catch (e) {
                errorDetail += ' Failed to read server error details.';
            }
            
            showMessage(`Login failed: ${errorDetail}`, 'error');
        }

    } catch (error) {
        console.error('Fetch error:', error);
        
        let displayError = 'Could not connect to the API server.';
        
        if (window.location.protocol === 'https:' && apiUrl.startsWith('http:')) {
            displayError = 'BLOCKED: Mixed Content. The secure HTTPS page cannot load the HTTP API.';
        }
        
        showMessage(displayError, 'error');
    }
});