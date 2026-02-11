let imageFile = null;

document.getElementById("imageInput").addEventListener("change", (e) => {
  imageFile = e.target.files[0];

  document.getElementById("error").innerText = "";
  document.getElementById("result").innerText = "";
  document.getElementById("confidence").innerText = "";

  if (imageFile) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(imageFile);

    const preview = document.getElementById("preview");
    preview.innerHTML = "";
    preview.appendChild(img);
  }
});

async function sendPrediction() {
  if (!imageFile) {
    document.getElementById("error").innerText = "Please upload an image first 🌼";
    return;
  }

  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    const API_BASE = "http://13.48.178.117:5000";

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    document.getElementById("result").innerText =
      "🌸 Prediction: " + data.prediction;
    document.getElementById("confidence").innerText =
      "🔍 Confidence: " + data.confidence;

  } catch (err) {
    document.getElementById("error").innerText = "Prediction failed 😢";
  }
}