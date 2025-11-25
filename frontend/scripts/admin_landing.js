import { BACKEND_URL } from "./config.js";
import { DOM_MESSAGES } from "../lang/en/messages.js";

const t = DOM_MESSAGES.adminLanding;

const modal = document.getElementById('confirmationModal');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
const userNameToDeleteElement = document.getElementById('userNameToDelete');

let userToDeleteData = { id: null, email: '' };

function openDeleteModal(userId, userEmail) {
    userToDeleteData = { id: userId, email: userEmail };
    userNameToDeleteElement.textContent = userEmail;
    modal.style.display = 'block';
}

function closeDeleteModal() {
    userToDeleteData = { id: null, email: '' };
    modal.style.display = 'none';
}

async function deleteUser() {
    const userId = userToDeleteData.id;
    const userEmail = userToDeleteData.email;

    if (!userId) return;

    try {
        const response = await fetch(`${BACKEND_URL}/admin/user/${userId}`, {
            method: "DELETE",
            credentials: "include",
        });

        if (response.status === 401) {
            window.location.href = "admin_login.html";
            return;
        }

        if (response.ok) {
            alert(`User ${userEmail} deleted successfully.`);
            loadUsers(); 
        } else {
            const errorText = await response.text();
            alert(`Failed to delete user ${userEmail}. Status: ${response.status}. Message: ${errorText}`);
        }
    } catch (error) {
        console.error(`Error deleting user ${userEmail}:`, error);
        alert(`An unexpected error occurred while deleting user ${userEmail}.`);
    }
}

async function updateApiRequests(userId, userEmail) {
    const newValueStr = prompt(`Enter the API Requests for user ${userEmail}:`);
    
    if (newValueStr === null || newValueStr.trim() === "") {
        return;
    }

    const newValue = parseInt(newValueStr.trim(), 10);

    if (isNaN(newValue) || newValue < 0) {
        alert("Invalid input. Please enter a non-negative number.");
        return;
    }

    const updateUrl = `${BACKEND_URL}/admin/user/${userId}/requests?requests_remaining=${newValue}`;

    try {
        const response = await fetch(updateUrl, {
            method: "PATCH", 
            credentials: "include",
        });

        if (response.status === 401) {
            window.location.href = "admin_login.html";
            return;
        }

        if (response.ok) {
            alert(`API Requests updated successfully for user ${userEmail} to ${newValue}.`);
            loadUsers(); 
        } else {
            const errorText = await response.text();
            alert(`Failed to update API Requests for ${userEmail}. Status: ${response.status}. Message: ${errorText}`);
        }
    } catch (error) {
        console.error(`Error updating API requests for ${userEmail}:`, error);
        alert(`An unexpected error occurred while updating API requests for ${userEmail}.`);
    }
}

async function loadUsers() {
  const tableBody = document.getElementById("userTableBody");
  tableBody.innerHTML = `<tr><td colspan="5">${t.loading}</td></tr>`;

  try {
    const response = await fetch(`${BACKEND_URL}/admin/users`, {
      method: "GET",
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "admin_login.html";
      return;
    }

    if (!response.ok) throw new Error(t.fetchError);
    const users = await response.json();

    tableBody.innerHTML = "";

    if (users.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="2">${t.loading}: No users found</td></tr>`;
      return;
    }

    users.forEach((user) => {
      const row = document.createElement("tr");

      const deleteButtonHtml = `
            <button class="delete-btn" data-user-id="${user.id}" data-user-email="${user.email}" style="margin-right: 5px;">
                Delete
            </button>
      `;

      const updateButtonHtml = `
            <button class="update-btn" data-user-id="${user.id}" data-user-email="${user.email}">
                Update API
            </button>
      `;

      row.innerHTML = `
        <td>${user.email}</td>
        <td>${user.last_jwt}</td>
        <td>${user.api_requests_left}</td>
        <td>${user.total_api_calls}</td>
        <td>
            ${updateButtonHtml}
            ${deleteButtonHtml}
        </td>
      `;
      tableBody.appendChild(row);

      const deleteButton = row.querySelector('.delete-btn');
      deleteButton.addEventListener('click', () => {
          // Open the modal, passing the user's ID and Email
          openDeleteModal(user.id, user.email);
      });
      const updateButton = row.querySelector('.update-btn');
      updateButton.addEventListener('click', () => {
          updateApiRequests(user.id, user.email);
      });
    });
  } catch (error) {
    tableBody.innerHTML = `
      <tr><td colspan="5" style="color:red;">${t.loadingError}: ${error.message}</td></tr>
    `;
  }
}

async function loadEndpoints() {
  const tableBody = document.getElementById("endpointTableBody");
  tableBody.innerHTML = `<tr><td colspan="3">${t.loadingEndpoint}</td></tr>`;

  try {
    const response = await fetch(`${BACKEND_URL}/admin/endpoint_access`, {
      method: "GET",
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "admin_login.html";
      return;
    }

    if (!response.ok) throw new Error(t.fetchError);

    const endpoints = await response.json();
    tableBody.innerHTML = "";

    if (endpoints.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="3">${t.loading}: ${t.endpointError}</td></tr>`;
      return;
    }

    endpoints.forEach(ep => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${ep.method}</td>
        <td>${ep.endpoint}</td>
        <td>${ep.requests}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    tableBody.innerHTML = `
      <tr><td colspan="3" style="color:red;">${t.loadingError}: ${error.message}</td></tr>
    `;
  }
}

function loadStaticText() {
  document.title = t.title;
  document.getElementById("greeting").textContent = t.title;
  document.getElementById("userOverviewHeader").textContent = t.h2;
  document.getElementById("endpointHeading").textContent = t.h2Endpoint;

  const endpointHeaders = document.querySelectorAll("#endpointTable thead th");
  if (endpointHeaders.length === 3) {
    endpointHeaders[0].textContent = t.colMethod;
    endpointHeaders[1].textContent = t.colEndpoint;
    endpointHeaders[2].textContent = t.colEndpointRequests;
  }

  const headers = document.querySelectorAll("#userTable thead th");
  if (headers.length >= 2) {
    headers[0].textContent = t.colUserName;
    headers[1].textContent = t.colLastJwt;
    headers[2].textContent = t.colRemainingApiRequests;
    headers[3].textContent = t.colConsumedApiRequests;
    headers[4].textContent = 'Actions';
  }

  document.getElementById("logoutBtn").textContent = t.logoutButton;
}

async function logout() {
  try {
    await fetch(`${BACKEND_URL}/admin/logout`, {
      method: "POST",
      credentials: "include",
    });
  } catch (err) {
    console.error(t.logoutFailed, err);
  } finally {
    window.location.href = "admin_login.html";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadStaticText();
  loadUsers();
  loadEndpoints();

  document.getElementById("logoutBtn").addEventListener("click", logout);

  cancelDeleteBtn.addEventListener('click', closeDeleteModal);
  confirmDeleteBtn.addEventListener('click', async () => {
    // Perform deletion and then close the modal
    await deleteUser(); 
    closeDeleteModal();
  });

  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeDeleteModal();
    }
  });
});
