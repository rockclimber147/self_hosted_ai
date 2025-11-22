import { BACKEND_URL } from "./config.js";
import {DOM_MESSAGES} from "../lang/en/messages.js"

const t = DOM_MESSAGES.customerLanding;

async function loadUser() {
  try {
    const response = await fetch(`${BACKEND_URL}/user/get_user_info`, {
      method: "GET",
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "customer_login.html";
      return;
    }

    if (!response.ok) throw new Error(t.errorLoadUser);
    const user = await response.json();
    console.log(user);
    return user;
  } catch (error) {
    console.log(error);
  }
}

function loadStaticText() {
  document.title = t.title;
  document.getElementById("h1").textContent = t.h1;
  document.getElementById("labelUser").textContent = t.user;
  document.getElementById("labelApiLeft").textContent = t.apiRequestLeft;
  document.getElementById("uploadDescription").textContent = t.uploadDescription;
  document.getElementById("uploadLabel").textContent = t.uploadLabel;
  document.getElementById("uploadBtn").textContent = t.uploadButton;
  document.getElementById("loading").textContent = t.loading;
  document.getElementById("h3Summary").textContent = t.h3Summary;
  document.getElementById("h3AIResponse").textContent = t.h3AIResponse;
  document.getElementById("responseText").textContent = t.defaultResponse;
  document.getElementById("logoutBtn").textContent = t.logoutButton;
}

document.addEventListener("DOMContentLoaded", async () => {
  loadStaticText();

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
      alert(t.alert);
      return;
    }

    loadingDiv.classList.remove("hidden");
    resultDiv.classList.add("hidden");
    errorDiv.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${BACKEND_URL}/ai/summarize/`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(t.serverError + `${response.status} - ${text}`);
      }
      const data = await response.json();

      loadingDiv.classList.add("hidden");
      resultDiv.classList.remove("hidden");
      summaryText.textContent = data.summary || t.summaryDefault;
      responseText.textContent = JSON.stringify(data, null, 2);

      // let count = parseInt(apiCount.textContent);
      // apiCount.textContent = count;
    } catch (err) {
      loadingDiv.classList.add("hidden");
      errorDiv.classList.remove("hidden");
      errorDiv.textContent = t.uploadError + err.message;
    }
  });

  document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch(`${BACKEND_URL}/user/logout`, {
      method: "POST",
      credentials: "include",
    });
    window.location.href = "customer_login.html";
  });
});
