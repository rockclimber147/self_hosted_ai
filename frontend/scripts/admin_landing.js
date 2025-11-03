import { BACKEND_URL } from "./config.js";

document.getElementById("greeting").textContent = "Admin Dashboard";

async function loadUsers() {
  try {
    const response = await fetch(`${BACKEND_URL}/admin/users`, {
      method: "GET",
      credentials: "include"
    });

    if (response.status === 401) {
      window.location.href = "admin_login.html";
      return;
    }

    if (!response.ok) throw new Error("Failed to fetch user list");
    const users = await response.json();

    const tableBody = document.getElementById("userTableBody");
    tableBody.innerHTML = "";
    
    users.forEach(user => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${user.email}</td>
        <td>${user.api_requests_left}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    document.getElementById("userTableBody").innerHTML = `
      <tr><td colspan="2" style="color:red;">Error loading users: ${error.message}</td></tr>
    `;
  }
}

loadUsers();

document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch(`${BACKEND_URL}/admin/logout`, {
      method: "POST",
      credentials: "include"
    });
    window.location.href = "admin_login.html";
  });
  