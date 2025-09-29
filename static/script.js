document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('summaryForm');
    const inputText = document.getElementById('inputText');
    const charCount = document.getElementById('charCount');
    const modeSelect = document.getElementById('mode');
    const lengthInput = document.getElementById('length');
    const outputDiv = document.getElementById('output');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Character counter
    inputText.addEventListener('input', function() {
        charCount.textContent = inputText.value.length + ' / 2000 characters';
        if (inputText.value.length > 2000) {
            charCount.style.color = 'red';
        } else {
            charCount.style.color = '#666';
        }
    });

    // Toggle length input visibility based on mode
    modeSelect.addEventListener('change', function() {
        const lengthLabel = lengthInput.parentElement;
        if (modeSelect.value === 'abstractive') {
            lengthLabel.style.display = 'none';
        } else {
            lengthLabel.style.display = 'block';
        }
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const text = inputText.value.trim();
        if (!text) {
            showError('Please enter some text to summarize.');
            return;
        }

        if (text.length > 2000) {
            showError('Text exceeds 2000 characters. Please shorten it.');
            return;
        }

        const mode = modeSelect.value;
        const length = mode === 'extractive' ? parseInt(lengthInput.value) || 3 : null;

        // Disable button and show loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Summarizing...';
        showLoading('Processing your text...');

        try {
            const response = await fetch('/summarize', {  // Backend endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    mode: mode,
                    length: length  // Only used for extractive
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                showError(data.error);
            } else {
                showSummary(data.summary, mode);
            }
        } catch (error) {
            showError('Failed to summarize. Please try again or check the server.');
            console.error('Error:', error);
        } finally {
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Summarize';
        }
    });

    // Helper functions
    function showSummary(summary, mode) {
        outputDiv.innerHTML = `
            <h3>Summary (${mode.charAt(0).toUpperCase() + mode.slice(1)} Mode):</h3>
            <div class="summary">${summary.replace(/\n/g, '<br>')}</div>
        `;
        outputDiv.classList.add('show');
    }

    function showError(message) {
        outputDiv.innerHTML = `<div class="error">Error: ${message}</div>`;
        outputDiv.classList.add('show');
    }

    function showLoading(message) {
        outputDiv.innerHTML = `<div class="loading">${message}</div>`;
        outputDiv.classList.add('show');
    }

    // Initial hide length if abstractive is default
        modeSelect.addEventListener('change', function() {
        const lengthGroup = document.getElementById('lengthGroup');
        if (modeSelect.value === 'abstractive') {
            lengthGroup.style.display = 'none';
        } else {
            lengthGroup.style.display = 'block';  // Or 'flex' if you update CSS
        }
    });
// ... (and at the end:)
    // Initial hide length if abstractive is default
    if (modeSelect.value === 'abstractive') {
        document.getElementById('lengthGroup').style.display = 'none';
    }
});