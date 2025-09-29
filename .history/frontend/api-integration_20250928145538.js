"""
API Integration for existing frontend
This file modifies the existing functions to use real API calls
"""

// Override the existing simulateProcessing function to use real API
window.originalSimulateProcessing = window.simulateProcessing;

// Replace simulateProcessing with real API calls
window.simulateProcessing = async function() {
    try {
        console.log('Starting real API processing...');
        
        // Check API health first
        const health = await apiClient.checkHealth();
        if (health.status !== 'healthy') {
            throw new Error('API is not healthy');
        }
        
        let result;
        
        // Process based on current layer
        if (currentLayer === 1) {
            console.log('Processing with Layer 1 (Fast Mode)');
            updateStepStatus('step-analyze', 'active');
            result = await apiClient.processLayer1(uploadedFile);
            
        } else if (currentLayer === 2) {
            console.log('Processing with Layer 2 (Config Mode)');
            updateStepStatus('step-analyze', 'active');
            
            // Get configuration from UI elements
            const config = {
                chunking_method: document.getElementById('chunking-method')?.value || 'semantic',
                embedding_model: document.getElementById('embedding-model')?.value || 'all-MiniLM-L6-v2',
                batch_size: parseInt(document.getElementById('batch-size')?.value) || 64
            };
            
            result = await apiClient.processLayer2(uploadedFile, config);
            
        } else if (currentLayer === 3) {
            console.log('Processing with Layer 3 (Deep Config Mode)');
            // For Layer 3, we'll use the existing deep config workflow
            // but replace the mock functions with real API calls
            handleDeepConfigFileUpload(uploadedFile);
            return;
        }
        
        // Handle successful processing
        if (result && result.success) {
            console.log('Processing successful:', result);
            
            // Store result globally
            window.processedData = result;
            
            // Update all steps as completed with timing
            const steps = ['step-analyze', 'step-preprocess', 'step-chunking', 'step-embedding', 'step-storage', 'step-retrieval'];
            const stepDuration = 1000; // 1 second between steps for visual effect
            
            for (let i = 0; i < steps.length; i++) {
                setTimeout(() => {
                    updateStepStatus(steps[i], 'completed');
                }, i * stepDuration);
            }
            
            // Update processing time and stats
            setTimeout(() => {
                const processingTime = result.processing_summary?.processing_time_seconds || 
                                    ((Date.now() - processingStartTime) / 1000);
                updateProcessingTime(processingTime);
                updateStatsWithRealData(result);
                showRealDownloadButtons(result.download_links);
                enableRealQueryInterface(result.processing_id);
                
                // Complete processing
                completeProcessing();
            }, steps.length * stepDuration);
            
        } else {
            throw new Error(result?.error || 'Processing failed');
        }
        
    } catch (error) {
        console.error('API Processing failed:', error);
        
        // Show error
        updateStepStatus('step-analyze', 'error');
        alert(`Processing failed: ${error.message}\n\nFalling back to demo mode...`);
        
        // Fallback to original simulation
        if (window.originalSimulateProcessing) {
            window.originalSimulateProcessing();
        }
    }
};

// Update stats with real data
function updateStatsWithRealData(result) {
    const summary = result.processing_summary;
    if (!summary) return;
    
    // Update sidebar stats
    const stats = {
        rows: summary.input_data?.total_rows || 0,
        columns: summary.input_data?.total_columns || 0,
        chunks: summary.chunking_results?.total_chunks || 0,
        embeddings: summary.embedding_results?.total_embeddings || 0,
        time: `${summary.processing_time_seconds || 0}s`
    };
    
    Object.entries(stats).forEach(([key, value]) => {
        const element = document.querySelector(`[data-stat="${key}"]`);
        if (element) {
            element.textContent = value;
        }
    });
    
    console.log('Updated stats:', stats);
}

// Show real download buttons
function showRealDownloadButtons(downloadLinks) {
    if (!downloadLinks) return;
    
    // Find or create download section
    let downloadSection = document.getElementById('download-section');
    if (!downloadSection) {
        downloadSection = document.createElement('div');
        downloadSection.id = 'download-section';
        downloadSection.className = 'config-card';
        downloadSection.style.marginTop = '20px';
        downloadSection.innerHTML = `
            <div class="config-card-header">
                <div class="config-icon">📁</div>
                <div class="config-title">Download Processed Files</div>
            </div>
            <div id="download-buttons" class="form-group" style="display: flex; gap: 10px; flex-wrap: wrap;"></div>
        `;
        
        // Add to the active content section
        const activeSection = document.querySelector('.content-section.active .content-wrapper');
        if (activeSection) {
            activeSection.appendChild(downloadSection);
        }
    }
    
    // Create download buttons
    const buttonsContainer = document.getElementById('download-buttons');
    buttonsContainer.innerHTML = '';
    
    const buttonLabels = {
        chunks_csv: '📊 Chunks CSV',
        embeddings_json: '🧠 Embeddings JSON', 
        metadata_json: '📋 Metadata JSON',
        summary_json: '📈 Summary JSON',
        results_zip: '📦 All Files (ZIP)'
    };
    
    Object.entries(downloadLinks).forEach(([type, linkInfo]) => {
        const button = document.createElement('button');
        button.className = 'btn btn-secondary';
        button.innerHTML = buttonLabels[type] || `📄 ${type}`;
        button.style.minWidth = '150px';
        button.onclick = () => downloadRealFile(linkInfo.file_id, linkInfo.url);
        buttonsContainer.appendChild(button);
    });
    
    console.log('Added download buttons:', Object.keys(downloadLinks));
}

// Download real file
async function downloadRealFile(fileId, url) {
    try {
        console.log(`Downloading file: ${fileId}`);
        const filename = url.split('/').pop();
        await apiClient.downloadFile(fileId, filename);
        
        // Show success message
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '✅ Downloaded!';
        button.disabled = true;
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 2000);
        
    } catch (error) {
        console.error('Download failed:', error);
        alert(`Download failed: ${error.message}`);
    }
}

// Enable real query interface
function enableRealQueryInterface(processingId) {
    // Find or create search section
    let searchSection = document.getElementById('search-section');
    if (!searchSection) {
        searchSection = document.createElement('div');
        searchSection.id = 'search-section';
        searchSection.className = 'config-card';
        searchSection.style.marginTop = '20px';
        searchSection.innerHTML = `
            <div class="config-card-header">
                <div class="config-icon">🔍</div>
                <div class="config-title">Search Processed Data</div>
            </div>
            <div class="form-group">
                <input type="text" id="real-search-query" class="form-control" 
                       placeholder="Enter your search query..." style="margin-bottom: 10px;">
                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 10px;">
                    <select id="similarity-metric" class="form-control" style="flex: 1;">
                        <option value="cosine">Cosine Similarity</option>
                        <option value="dot">Dot Product</option>
                        <option value="euclidean">Euclidean Distance</option>
                    </select>
                    <input type="number" id="top-k" class="form-control" value="5" min="1" max="20" 
                           placeholder="Results" style="width: 100px;">
                </div>
                <button onclick="performRealSearch('${processingId}')" class="btn btn-primary">
                    🔍 Search Chunks
                </button>
            </div>
            <div id="real-search-results" class="search-results"></div>
        `;
        
        // Add to active content section
        const activeSection = document.querySelector('.content-section.active .content-wrapper');
        if (activeSection) {
            activeSection.appendChild(searchSection);
        }
    }
    
    // Add Enter key support
    const searchInput = document.getElementById('real-search-query');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performRealSearch(processingId);
            }
        });
    }
    
    console.log('Enabled real query interface for:', processingId);
}

// Perform real search
window.performRealSearch = async function(processingId) {
    const query = document.getElementById('real-search-query').value.trim();
    if (!query) {
        alert('Please enter a search query');
        return;
    }
    
    const similarityMetric = document.getElementById('similarity-metric').value;
    const topK = parseInt(document.getElementById('top-k').value) || 5;
    
    const resultsContainer = document.getElementById('real-search-results');
    resultsContainer.innerHTML = '<p>🔍 Searching...</p>';
    
    try {
        console.log(`Searching: "${query}" with ${similarityMetric} similarity`);
        
        const searchResults = await apiClient.searchChunks(processingId, query, {
            similarity_metric: similarityMetric,
            top_k: topK
        });
        
        if (searchResults.success && searchResults.results.length > 0) {
            displayRealSearchResults(searchResults.results, searchResults.query);
        } else {
            resultsContainer.innerHTML = '<p>No results found for your query.</p>';
        }
        
    } catch (error) {
        console.error('Search failed:', error);
        resultsContainer.innerHTML = `<p style="color: red;">Search failed: ${error.message}</p>`;
    }
};

// Display real search results
function displayRealSearchResults(results, query) {
    const resultsContainer = document.getElementById('real-search-results');
    
    const resultsHTML = `
        <div style="margin-top: 15px;">
            <h4>🔍 Search Results for "${query}" (${results.length} found)</h4>
            ${results.map((result, index) => `
                <div class="search-result-item" style="
                    border: 1px solid #e5e7eb; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 10px 0;
                    background: #f9fafb;
                ">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 8px;">
                        <strong>Result ${index + 1}</strong>
                        <span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                            Score: ${(result.similarity_score || 0).toFixed(3)}
                        </span>
                    </div>
                    <p><strong>Chunk ID:</strong> <code>${result.chunk_id}</code></p>
                    <p><strong>Content:</strong></p>
                    <div style="background: white; padding: 10px; border-radius: 4px; border-left: 3px solid #10b981; font-family: monospace; font-size: 14px; max-height: 100px; overflow-y: auto;">
                        ${result.document || 'No content available'}
                    </div>
                    ${result.metadata ? `
                        <details style="margin-top: 8px;">
                            <summary style="cursor: pointer; color: #6b7280;">Metadata</summary>
                            <pre style="background: #f3f4f6; padding: 8px; border-radius: 4px; font-size: 12px; margin-top: 5px;">${JSON.stringify(result.metadata, null, 2)}</pre>
                        </details>
                    ` : ''}
                </div>
            `).join('')}
        </div>
    `;
    
    resultsContainer.innerHTML = resultsHTML;
    console.log('Displayed search results:', results.length);
}

// Initialize API integration when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔗 API Integration loaded');
    
    // Check API connection
    apiClient.checkHealth().then(health => {
        console.log('API Health:', health);
        if (health.status === 'healthy') {
            console.log('✅ Connected to FastAPI backend');
        } else {
            console.warn('⚠️ API connection issues, will use demo mode');
        }
    }).catch(error => {
        console.warn('⚠️ Cannot connect to API, using demo mode:', error.message);
    });
});

console.log('🔗 API Integration script loaded');
