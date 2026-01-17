const analyzeBtn = document.getElementById('analyzeBtn');
const inputText = document.getElementById('inputText');
const resultBody = document.getElementById('resultBody');
const errorMsg = document.getElementById('errorMsg');

// POS tag descriptions
const tagMap = {
  AUX: "Auxiliary Verb",
  CC: "Conjunction",
  CD: "Cardinal Number",
  DT: "Determiner",
  IN: "Preposition",
  JJ: "Adjective",
  NN: "Noun",
  PA: "Particle",
  PN: "Proper Noun",
  PRO: "Pronoun",
  RB: "Adverb",
  SYM: "Symbol",
  VB: "Verb",
  O: "None"
};

function getPosDescription(tag) {
  return tagMap[tag.toUpperCase()] || "Unknown";
}

function showError(message) {
  errorMsg.innerText = message;
  errorMsg.style.display = 'block';
  inputText.style.border = '1px solid #c62828';
}

function clearError() {
  errorMsg.style.display = 'none';
  inputText.style.border = '1px solid #ccc';
}

analyzeBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();

  // Validation
  if (!text) {
    showError("Please enter some Khmer text before analyzing.");
    inputText.focus();
    return;
  }

  clearError();

  // Loading UI
  analyzeBtn.disabled = true;
  analyzeBtn.innerText = "Analyzing...";
  resultBody.innerHTML =
    '<tr><td colspan="4">Processing...</td></tr>';

  try {
    const response = await fetch('http://127.0.0.1:8000/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();
    resultBody.innerHTML = '';

    if (!data.tokens || data.tokens.length === 0) {
      resultBody.innerHTML =
        '<tr><td colspan="4">No tokens returned.</td></tr>';
      return;
    }

    data.tokens.forEach((item, index) => {
      resultBody.innerHTML += `
        <tr>
          <td>${index + 1}</td>
          <td class="khmer-text">${item.word}</td>
          <td><b style="color:#1f3c88;">${item.tag}</b></td>
          <td>${getPosDescription(item.tag)}</td>
        </tr>
      `;
    });

  } catch (error) {
    console.error(error);
    resultBody.innerHTML =
      `<tr>
        <td colspan="4" style="color:#c62828;">
          ❌ Cannot connect to backend.  
          Please make sure FastAPI is running.
        </td>
      </tr>`;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = "Analyze Text";
  }
});
