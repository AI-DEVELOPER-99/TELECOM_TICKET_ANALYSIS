// API URL
const API_URL = '';

// Check backend status on load
async function checkBackendStatus() {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');

    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        if (data.initialized) {
            statusIndicator.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusIndicator.classList.add('error');
            statusText.textContent = 'Backend not initialized';
        }
    } catch (error) {
        statusIndicator.classList.add('error');
        statusText.textContent = 'Backend offline';
    }
}

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');

    // Load stats if stats tab is selected
    if (tabName === 'stats') {
        loadStats();
    }
}

// Analyze form handler
document.getElementById('analyze-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const subject = document.getElementById('ticket-subject').value;
    const description = document.getElementById('ticket-description').value;
    const ticketDescription = `Subject: ${subject}\n\nDescription: ${description}`;

    const btn = e.target.querySelector('.btn');
    const btnText = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.spinner');

    // Show loading state
    btn.disabled = true;
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'inline-block';

    // Hide previous results
    document.getElementById('analyze-results').style.display = 'none';

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket_description: ticketDescription })
        });

        const data = await response.json();

        if (data.success) {
            displayAnalysisResults(data);
        } else {
            showError('analyze-results', data.error || 'Analysis failed');
        }
    } catch (error) {
        showError('analyze-results', 'Network error. Please check if backend is running.');
    } finally {
        // Reset button
        btn.disabled = false;
        btnText.textContent = 'Analyze Ticket';
        spinner.style.display = 'none';
    }
});

// Display analysis results
function displayAnalysisResults(data) {
    const resultsContainer = document.getElementById('analyze-results');
    resultsContainer.style.display = 'block';

    let html = `
        <div class="card">
            <h2>Analysis Results</h2>
            <p class="description">Based on ${data.similar_tickets_count} similar resolved tickets</p>
        </div>
    `;

    data.solutions.forEach(solution => {
        const percentage = solution.suitability_percentage;
        let suitabilityClass = 'suitability-low';
        if (percentage >= 75) suitabilityClass = 'suitability-high';
        else if (percentage >= 50) suitabilityClass = 'suitability-medium';

        html += `
            <div class="solution-card rank-${solution.rank}">
                <div class="solution-header">
                    <div class="solution-rank">Solution #${solution.rank}</div>
                    <div class="suitability-badge ${suitabilityClass}">
                        ${percentage}% Suitable
                    </div>
                </div>
                <div class="solution-text">
                    ${escapeHtml(solution.solution)}
                </div>
                <div class="solution-meta">
                    <p><strong>Reasoning:</strong> ${escapeHtml(solution.reasoning)}</p>
                    ${solution.reference_tickets && solution.reference_tickets.length > 0 
                        ? `<p><strong>References:</strong> Similar tickets #${solution.reference_tickets.join(', #')}</p>`
                        : ''}
                </div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Search form handler
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = document.getElementById('search-query').value;
    const topK = parseInt(document.getElementById('top-k').value);

    const btn = e.target.querySelector('.btn');
    const btnText = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.spinner');

    // Show loading state
    btn.disabled = true;
    btnText.textContent = 'Searching...';
    spinner.style.display = 'inline-block';

    // Hide previous results
    document.getElementById('search-results').style.display = 'none';

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, top_k: topK })
        });

        const data = await response.json();

        if (data.success) {
            displaySearchResults(data.results);
        } else {
            showError('search-results', data.error || 'Search failed');
        }
    } catch (error) {
        showError('search-results', 'Network error. Please check if backend is running.');
    } finally {
        // Reset button
        btn.disabled = false;
        btnText.textContent = 'Search';
        spinner.style.display = 'none';
    }
});

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.style.display = 'block';

    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="card">
                <p>No results found.</p>
            </div>
        `;
        return;
    }

    let html = `
        <div class="card">
            <h2>Search Results</h2>
            <p class="description">Found ${results.length} similar tickets</p>
        </div>
    `;

    results.forEach((result, index) => {
        const similarity = Math.round(result.similarity_score * 100);
        const resultId = `result-${index}`;
        
        html += `
            <div class="search-result">
                <h3>${index + 1}. ${escapeHtml(result.subject)}</h3>
                <div class="search-result-meta">
                    <span class="badge badge-similarity">Similarity: ${similarity}%</span>
                    <span class="badge badge-type">${escapeHtml(result.type)}</span>
                    <span class="badge badge-priority">${escapeHtml(result.priority)}</span>
                    ${result.queue ? `<span class="badge">${escapeHtml(result.queue)}</span>` : ''}
                </div>
                <div class="ticket-details">
                    <div class="detail-section">
                        <strong>Description:</strong>
                        <p class="ticket-body">${escapeHtml(result.body)}</p>
                    </div>
                    ${result.answer ? `
                    <div class="detail-section">
                        <strong>Resolution:</strong>
                        <p class="ticket-answer">${escapeHtml(result.answer)}</p>
                    </div>
                    ` : ''}
                    ${result.tags && result.tags.length > 0 ? `
                    <div class="detail-section">
                        <strong>Tags:</strong> ${result.tags.map(tag => `<span class="badge">${escapeHtml(tag)}</span>`).join(' ')}
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Load statistics
async function loadStats() {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '<p>Loading statistics...</p>';

    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;
            statsContent.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">${stats.total_tickets.toLocaleString()}</div>
                        <div class="stat-label">Total Tickets</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.embedding_dimension}</div>
                        <div class="stat-label">Embedding Dimension</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" style="font-size: 1.5rem;">${stats.embedding_model}</div>
                        <div class="stat-label">Embedding Model</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" style="font-size: 1.5rem;">${stats.llm_model}</div>
                        <div class="stat-label">LLM Model</div>
                    </div>
                </div>
            `;
        } else {
            statsContent.innerHTML = `<p class="alert alert-error">Failed to load statistics</p>`;
        }
    } catch (error) {
        statsContent.innerHTML = `<p class="alert alert-error">Network error. Please check if backend is running.</p>`;
    }
}

// Show error message
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.style.display = 'block';
    container.innerHTML = `
        <div class="card">
            <div class="alert alert-error">
                <strong>Error:</strong> ${escapeHtml(message)}
            </div>
        </div>
    `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkBackendStatus();
});
