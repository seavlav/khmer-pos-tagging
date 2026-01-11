document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('inputText').value;
    const resultBody = document.getElementById('resultBody');
    const btn = document.getElementById('analyzeBtn');

    if (!text.trim()) {
        alert("Please enter some text.");
        return;
    }

    // Update UI to show loading state
    btn.disabled = true;
    btn.innerText = "Analyzing...";
    resultBody.innerHTML = '<tr><td colspan="4">Processing...</td></tr>';

    try {
        const response = await fetch('http://127.0.0.1:8000/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) throw new Error('Backend server error');

        const data = await response.json();
        
        // Clear table and inject new rows
        resultBody.innerHTML = "";
        data.tokens.forEach((item, index) => {
            const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td style="font-family: 'Kantumruy Pro', sans-serif;">${item.word}</td>
                    <td><b style="color: #1f3c88;">${item.tag}</b></td>
                    <td>${getPosDescription(item.tag)}</td>
                </tr>
            `;
            resultBody.innerHTML += row;
        });

    } catch (error) {
        console.error("Error:", error);
        resultBody.innerHTML = '<tr><td colspan="4" style="color:red;">Error connecting to backend. Ensure FastAPI is running.</td></tr>';
    } finally {
        btn.disabled = false;
        btn.innerText = "Analyze Text";
    }
});
