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
});
