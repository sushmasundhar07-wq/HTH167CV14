// ============================================================
// CROP DISEASE PREDICTION FRONTEND
// ============================================================

// ============================================================
// ELEMENTS
// ============================================================

const imageInput = document.getElementById("imageInput");

const imagePreview = document.getElementById("imagePreview");

const previewContainer = document.getElementById("previewContainer");

const uploadArea = document.getElementById("uploadArea");

const removeButton = document.getElementById("removeButton");

const analyzeButton = document.getElementById("analyzeButton");

const loading = document.getElementById("loading");

const resultCard = document.getElementById("resultCard");

const errorMessage = document.getElementById("errorMessage");

const errorText = document.getElementById("errorText");

// Result fields

const resultCrop = document.getElementById("resultCrop");

const resultDisease = document.getElementById("resultDisease");

const resultConfidence = document.getElementById("resultConfidence");

const resultSeverity = document.getElementById("resultSeverity");

const resultLoss = document.getElementById("resultLoss");

const resultCost = document.getElementById("resultCost");

const resultUrgency = document.getElementById("resultUrgency");

const resultSpread = document.getElementById("resultSpread");

const resultAction = document.getElementById("resultAction");

const farmerMessage = document.getElementById("farmerMessage");

const speakButton = document.getElementById("speakButton");

const priorityButton = document.getElementById("priorityButton");

const treatedButton = document.getElementById("treatedButton");

// ============================================================
// CURRENT RESULT
// ============================================================

let currentResult = null;

// ============================================================
// ADVISORY INFORMATION
//
// These are temporary UI values.
// The disease and confidence come from the ML backend.
// ============================================================

const advisoryData = {
  Tomato: {
    severity: "High",
    loss: 25,
    cost: 8500,
    urgency: "Immediate",
    spread: "High",
    action: "Inspect affected plants and begin appropriate treatment.",
  },

  Potato: {
    severity: "Medium",
    loss: 18,
    cost: 6500,
    urgency: "High",
    spread: "Medium",
    action: "Inspect the crop and begin disease management.",
  },

  Maize: {
    severity: "Low",
    loss: 5,
    cost: 3500,
    urgency: "Monitor",
    spread: "Low",
    action: "Monitor the crop regularly for changes.",
  },

  Apple: {
    severity: "Medium",
    loss: 15,
    cost: 5500,
    urgency: "High",
    spread: "Medium",
    action: "Inspect the crop and manage possible disease spread.",
  },

  Grape: {
    severity: "Medium",
    loss: 12,
    cost: 4800,
    urgency: "Moderate",
    spread: "Medium",
    action: "Monitor the crop and seek agricultural guidance.",
  },

  Pepper: {
    severity: "Low",
    loss: 6,
    cost: 3000,
    urgency: "Monitor",
    spread: "Low",
    action: "Monitor the crop regularly.",
  },

  Default: {
    severity: "Unknown",
    loss: 0,
    cost: 0,
    urgency: "Monitor",
    spread: "Unknown",
    action: "Consult an agricultural expert for further guidance.",
  },
};

// ============================================================
// FILE SELECTION
// ============================================================

imageInput.addEventListener("change", function () {
  hideError();

  const file = imageInput.files[0];

  if (!file) {
    return;
  }

  // Check image type

  if (!file.type.startsWith("image/")) {
    showError("Please select a valid image file.");

    imageInput.value = "";

    return;
  }

  // Check size

  const maxSize = 10 * 1024 * 1024;

  if (file.size > maxSize) {
    showError("Image size must be less than 10 MB.");

    imageInput.value = "";

    return;
  }

  // Show preview

  const reader = new FileReader();

  reader.onload = function (event) {
    imagePreview.src = event.target.result;

    previewContainer.style.display = "block";
  };

  reader.readAsDataURL(file);

  hideResult();
});

// ============================================================
// REMOVE IMAGE
// ============================================================

removeButton.addEventListener("click", function () {
  imageInput.value = "";

  imagePreview.src = "";

  previewContainer.style.display = "none";

  hideResult();

  hideError();
});

// ============================================================
// ANALYZE BUTTON
// ============================================================

analyzeButton.addEventListener("click", analyzeDisease);

// ============================================================
// MAIN PREDICTION FUNCTION
// ============================================================

async function analyzeDisease() {
  hideError();

  const file = imageInput.files[0];

  // --------------------------------------------------------
  // Validate image
  // --------------------------------------------------------

  if (!file) {
    showError("Please select a crop leaf image first.");

    return;
  }

  // --------------------------------------------------------
  // Disable button
  // --------------------------------------------------------

  analyzeButton.disabled = true;

  analyzeButton.textContent = "🔄 Analyzing...";

  loading.style.display = "block";

  resultCard.style.display = "none";

  // --------------------------------------------------------
  // Prepare image
  // --------------------------------------------------------

  const formData = new FormData();

  formData.append("image", file);

  try {
    console.log("Sending image to /predict...");

    // ----------------------------------------------------
    // SEND TO FLASK BACKEND
    // ----------------------------------------------------

    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    console.log("Backend status:", response.status);

    // ----------------------------------------------------
    // Read response
    // ----------------------------------------------------

    const data = await response.json();

    console.log("Backend response:", data);

    // ----------------------------------------------------
    // Check backend error
    // ----------------------------------------------------

    if (!response.ok || data.success === false) {
      throw new Error(data.error || "Prediction failed.");
    }

    // ----------------------------------------------------
    // Extract prediction
    // ----------------------------------------------------

    const disease =
      data.prediction ||
      data.disease ||
      data.class_name ||
      data.predicted_class;

    if (!disease) {
      throw new Error("Backend did not return a disease prediction.");
    }

    // ----------------------------------------------------
    // Confidence
    // ----------------------------------------------------

    const confidence = formatConfidence(data.confidence);

    // ----------------------------------------------------
    // Determine crop
    // ----------------------------------------------------

    const crop = detectCrop(disease);

    // ----------------------------------------------------
    // Advisory information
    // ----------------------------------------------------

    const advisory = advisoryData[crop] || advisoryData.Default;

    // ----------------------------------------------------
    // Build result
    // ----------------------------------------------------

    currentResult = {
      crop: crop,

      disease: formatDiseaseName(disease),

      confidence: confidence,

      severity: data.severity || advisory.severity,

      loss: data.loss !== undefined ? data.loss : advisory.loss,

      cost: data.cost !== undefined ? data.cost : advisory.cost,

      urgency: data.urgency || advisory.urgency,

      spread: data.spread || advisory.spread,

      action: data.action || advisory.action,
    };

    // ----------------------------------------------------
    // Display result
    // ----------------------------------------------------

    displayResult(currentResult);

    console.log("Prediction successful:", currentResult);
  } catch (error) {
    console.error("Prediction error:", error);

    showError("Could not connect to the prediction backend. " + error.message);
  } finally {
    loading.style.display = "none";

    analyzeButton.disabled = false;

    analyzeButton.textContent = "🔍 Analyze Crop Disease";
  }
}

// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(data) {
  resultCrop.textContent = data.crop;

  resultDisease.textContent = data.disease;

  resultConfidence.textContent = data.confidence;

  resultSeverity.textContent = data.severity;

  resultLoss.textContent = data.loss + "%";

  resultCost.textContent = "₹" + Number(data.cost).toLocaleString("en-IN");

  resultUrgency.textContent = data.urgency;

  resultSpread.textContent = data.spread;

  resultAction.textContent = data.action;

  farmerMessage.textContent =
    "The AI model detected " +
    data.disease +
    " with " +
    data.confidence +
    " confidence. " +
    data.action;

  resultCard.style.display = "block";

  resultCard.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

// ============================================================
// FORMAT DISEASE NAME
// ============================================================

function formatDiseaseName(name) {
  return String(name)
    .replace(/___/g, " - ")

    .replace(/_/g, " ")

    .replace(/\s+/g, " ")

    .trim();
}

// ============================================================
// FORMAT CONFIDENCE
// ============================================================

function formatConfidence(value) {
  if (value === undefined || value === null) {
    return "N/A";
  }

  const text = String(value).trim();

  // Already formatted

  if (text.includes("%")) {
    return text;
  }

  let number = Number(value);

  if (Number.isNaN(number)) {
    return text;
  }

  // Convert 0.94 → 94%

  if (number <= 1) {
    number *= 100;
  }

  return number.toFixed(2) + "%";
}

// ============================================================
// DETECT CROP
// ============================================================

function detectCrop(disease) {
  const text = String(disease).toLowerCase();

  if (text.includes("tomato")) {
    return "Tomato";
  }

  if (text.includes("potato")) {
    return "Potato";
  }

  if (text.includes("corn") || text.includes("maize")) {
    return "Maize";
  }

  if (text.includes("apple")) {
    return "Apple";
  }

  if (text.includes("grape")) {
    return "Grape";
  }

  if (text.includes("pepper")) {
    return "Pepper";
  }

  return "Unknown";
}

// ============================================================
// ERROR
// ============================================================

function showError(message) {
  errorText.textContent = message;

  errorMessage.style.display = "block";
}

function hideError() {
  errorMessage.style.display = "none";
}

// ============================================================
// HIDE RESULT
// ============================================================

function hideResult() {
  resultCard.style.display = "none";
}

// ============================================================
// VOICE
// ============================================================

speakButton.addEventListener("click", function () {
  if (!currentResult) {
    showError("Please analyze an image first.");

    return;
  }

  if (!("speechSynthesis" in window)) {
    showError("Voice output is not supported by this browser.");

    return;
  }

  const message =
    "Crop " +
    currentResult.crop +
    ". " +
    "Detected disease: " +
    currentResult.disease +
    ". " +
    "Confidence: " +
    currentResult.confidence +
    ". " +
    "Severity: " +
    currentResult.severity +
    ". " +
    "Recommended action: " +
    currentResult.action;

  speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(message);

  utterance.rate = 0.9;

  speechSynthesis.speak(utterance);
});

// ============================================================
// PRIORITY
// ============================================================

priorityButton.addEventListener("click", function () {
  if (!currentResult) {
    showError("Please analyze an image first.");

    return;
  }

  localStorage.setItem("priorityCrop", JSON.stringify(currentResult));

  alert("Crop added to priority list.");
});

// ============================================================
// MARK TREATED
// ============================================================

treatedButton.addEventListener("click", function () {
  if (!currentResult) {
    showError("Please analyze an image first.");

    return;
  }

  currentResult.treated = true;

  localStorage.setItem("treatedCrop", JSON.stringify(currentResult));

  alert("Crop marked as treated.");
});
