function analyzeImage() {
    const input = document.getElementById('imageInput');
    const resultsDiv = document.getElementById('results');
    const file = input.files[0];
    
    if (!file) {
        showError('Please select an image first');
        return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }

    // Validate file size (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (file.size > maxSize) {
        showError('Image size must be less than 5MB');
        return;
    }

    // Show loading state
    resultsDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing image...</div>';

    const reader = new FileReader();
    reader.onload = function(e) {
        // Send image to backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: e.target.result
            })
        })
        .then(async response => {
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `Server error (${response.status})`);
            }
            
            return data;
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error.message || 'Error analyzing image');
        });
    };

    reader.onerror = function(error) {
        console.error('FileReader error:', error);
        showError('Error reading the image file');
    };

    try {
        reader.readAsDataURL(file);
    } catch (error) {
        console.error('ReadAsDataURL error:', error);
        showError('Error processing the image file');
    }
}

function showError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="error">
            <i class="fas fa-exclamation-circle"></i>
            <h2>Error</h2>
            <p>${message}</p>
            <button onclick="dismissError()" class="dismiss-btn">
                <i class="fas fa-times"></i> Dismiss
            </button>
        </div>
    `;
}

function dismissError() {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    if (!data || typeof data !== 'object') {
        showError('Invalid response from server');
        return;
    }

    resultsDiv.innerHTML = `
        <div class="results-container">
            <h2>Analysis Results</h2>
            <div class="risk-level ${(data.risk_level || '').toLowerCase()}">
                <i class="fas ${data.risk_level?.toLowerCase() === 'high' ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i>
                <p>Risk Level: <span>${data.risk_level || 'Unknown'}</span></p>
            </div>
            <div class="indicators-section">
                <h3><i class="fas fa-list"></i> Suspicious Indicators:</h3>
                <ul>
                    ${Array.isArray(data.suspicious_indicators) && data.suspicious_indicators.length > 0 
                        ? data.suspicious_indicators.map(indicator => `<li><i class="fas fa-angle-right"></i>${indicator}</li>`).join('')
                        : '<li class="no-indicators"><i class="fas fa-check"></i>No suspicious indicators found</li>'
                    }
                </ul>
            </div>
            <div class="extracted-text">
                <h3><i class="fas fa-file-alt"></i> Extracted Text:</h3>
                <pre>${data.extracted_text || 'No text extracted'}</pre>
            </div>
        </div>
    `;
}


