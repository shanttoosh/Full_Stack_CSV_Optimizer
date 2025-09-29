"""
API Client for CSV Chunking Optimizer Pro Frontend
Connects the frontend to the FastAPI backend
"""

class APIClient 
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    /**
     * Convert file to base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                const base64 = reader.result.split(',')[1]; // Remove data:text/csv;base64, prefix
                resolve(base64);
            };
            reader.onerror = error => reject(error);
        });
    }

    /**
     * Process CSV using Layer 1 (Fast Mode)
     */
    async processLayer1(file) {
        try {
            const csvData = await this.fileToBase64(file);
            
            const response = await fetch(`${this.baseURL}/api/v1/layer1/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    csv_data: csvData,
                    filename: file.name
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Layer 1 processing failed:', error);
            throw error;
        }
    }

    /**
     * Process CSV using Layer 2 (Config Mode)
     */
    async processLayer2(file, options = {}) {
        try {
            const csvData = await this.fileToBase64(file);
            
            const requestBody = {
                csv_data: csvData,
                filename: file.name,
                ...options
            };

            const response = await fetch(`${this.baseURL}/api/v1/layer2/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Layer 2 processing failed:', error);
            throw error;
        }
    }

    /**
     * Process CSV using Layer 3 (Deep Config Mode)
     */
    async processLayer3(file, config = {}) {
        try {
            const csvData = await this.fileToBase64(file);
            
            const requestBody = {
                csv_data: csvData,
                filename: file.name,
                ...config
            };

            const response = await fetch(`${this.baseURL}/api/v1/layer3/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Layer 3 processing failed:', error);
            throw error;
        }
    }

    /**
     * Search processed chunks
     */
    async searchChunks(processingId, query, options = {}) {
        try {
            const requestBody = {
                query: query,
                model_name: options.model_name || 'all-MiniLM-L6-v2',
                top_k: options.top_k || 5,
                similarity_metric: options.similarity_metric || 'cosine'
            };

            const response = await fetch(`${this.baseURL}/api/v1/search/${processingId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Search failed:', error);
            throw error;
        }
    }

    /**
     * Download file by ID
     */
    async downloadFile(fileId, filename) {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/download/${fileId}`, {
                method: 'GET'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Create blob and download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = filename || fileId;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            return true;
        } catch (error) {
            console.error('Download failed:', error);
            throw error;
        }
    }

    /**
     * Check API health
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'unhealthy', error: error.message };
        }
    }

    /**
     * Get API info
     */
    async getAPIInfo() {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/info`);
            return await response.json();
        } catch (error) {
            console.error('API info failed:', error);
            throw error;
        }
    }
}

// Create global API client instance
window.apiClient = new APIClient();
