import { BACKEND_URL } from "./config.js";
import { DOM_MESSAGES } from "../lang/en/messages.js";

const t = DOM_MESSAGES.adminLanding;

async function loadUsers() {
  const tableBody = document.getElementById("userTableBody");
  tableBody.innerHTML = `<tr><td colspan="2">${t.loading}</td></tr>`;

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
      row.innerHTML = `
        <td>${user.email}</td>
        <td>${user.api_requests_left}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    tableBody.innerHTML = `
      <tr><td colspan="2" style="color:red;">${t.loadingError}: ${error.message}</td></tr>
    `;
  }
}

function loadStaticText() {
  document.title = t.title;
  document.getElementById("greeting").textContent = t.title;
  document.getElementById("userOverviewHeader").textContent = t.h2;

  const headers = document.querySelectorAll("#userTable thead th");
  if (headers.length >= 2) {
    headers[0].textContent = t.colUserName;
    headers[1].textContent = t.colRemainingApiRequests;
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
    console.error("Logout failed:", err);
  } finally {
    window.location.href = "admin_login.html";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadStaticText();
  loadUsers();

  document.getElementById("logoutBtn").addEventListener("click", logout);
});
