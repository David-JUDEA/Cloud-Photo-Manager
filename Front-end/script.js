const API_URL = "http://127.0.0.1:5001";

async function loadImages() {
  const gallery = document.getElementById("gallery");

  try {
    const response = await fetch(`${API_URL}/images`);
    const images = await response.json();

    gallery.innerHTML = "";

    if (images.length === 0) {
      gallery.innerHTML = "<p>No images available...</p>";
      return;
    }

    // Chaque image reçue, on crée le HTML
    images.forEach((image) => {
      const displayUrl = image.url.replace(
        "s3://cloud-photo-bucket",
        "http://localhost:4566/cloud-photo-bucket",
      );

      const displayName = image.filename.includes(".")
        ? image.filename.substring(0, image.filename.lastIndexOf("."))
        : image.filename;

      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
    	<img src="${displayUrl}" alt="${image.filename}">
        <p title="${image.filename}">${displayName}</p>
    	`;
      gallery.appendChild(card);
    });
  } catch (error) {
    console.error("Error:", error);
    gallery.innerHTML =
      '<p style="color:red">Unable to load images (Check if the backend is running)</p>';
  }
}

// Téléchargement d'une image
async function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const statusMessage = document.getElementById("statusMessage");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file !");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  statusMessage.textContent = "Sending...";

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      statusMessage.textContent = "✔ Image sent !";
      statusMessage.style.color = "lightgreen";
      fileInput.value = "";
      loadImages();
    } else {
      throw new Error("Error server");
    }
  } catch (error) {
    console.error(error);
    statusMessage.textContent = "✘ Error while sending.";
    statusMessage.style.color = "red";
  }
}

loadImages();
