import { URL } from "./config.js";

async function loadUser() {
  try {
    const response = await fetch(`${URL}/user/get_user_info`, {
      method: "GET",
      credentials: "include"
    });

    if (response.status === 401) {
      window.location.href = "customer_login.html";
      return;
    }

    if (!response.ok) throw new Error("Failed to fetch user list");
    const user = await response.json();
    console.log(user);
    return user;
  } catch (error) {
    console.log(error);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const user = await loadUser();
  const email = document.getElementById("email");
  email.textContent = user.email;

  const apiCount = document.getElementById("apiCount");
  apiCount.textContent = user.api_requests_left;

  const uploadBtn = document.getElementById("uploadBtn");
  const loadingDiv = document.getElementById("loading");
  const resultDiv = document.getElementById("result");
  const summaryText = document.getElementById("summaryText");
  const errorDiv = document.getElementById("error");
  const responseText = document.getElementById("responseText");

  uploadBtn.addEventListener("click", async () => {
    console.log("clicked");
    const fileInput = document.getElementById("videoFile");
    const file = fileInput.files[0];

    if (!file) {
      alert("Please select a video file first.");
      return;
    }

    loadingDiv.classList.remove("hidden");
    resultDiv.classList.add("hidden");
    errorDiv.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${URL}/ai/summarize/`, {
        method: "POST",
        body: formData,
        credentials: "include"
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Server error: ${response.status} - ${text}`);
      }
      const data = await response.json();

      loadingDiv.classList.add("hidden");
      resultDiv.classList.remove("hidden");
      summaryText.textContent = data.summary || "No summary generated.";
      responseText.textContent = JSON.stringify(data, null, 2);

      let count = parseInt(apiCount.textContent) + 1;
      apiCount.textContent = count;
    } catch (err) {
      loadingDiv.classList.add("hidden");
      errorDiv.classList.remove("hidden");
      errorDiv.textContent = "Error uploading video: " + err.message;
    }
  });

  document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch(`${URL}/user/logout`, {
      method: "POST",
      credentials: "include"
    });
    window.location.href = "customer_login.html";
  });
});
