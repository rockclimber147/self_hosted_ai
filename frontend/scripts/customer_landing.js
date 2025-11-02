
async function loadUser() {
  try {
    const response = await fetch("http://127.0.0.1:8000/user/get_user_info", {
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

  const uploadForm = document.getElementById("uploadForm");
  const loadingDiv = document.getElementById("loading");
  const resultDiv = document.getElementById("result");
  const summaryText = document.getElementById("summaryText");
  const errorDiv = document.getElementById("error");
  const responseText = document.getElementById("responseText");

  uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
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
      const response = await fetch("http://127.0.0.1:8000/ai/summarize", {
        method: "POST",
        body: formData,
        credentials: "include"
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);
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
    await fetch("http://127.0.0.1:8000/user/logout", {
      method: "POST",
      credentials: "include"
    });
    window.location.href = "customer_login.html";
  });
});
