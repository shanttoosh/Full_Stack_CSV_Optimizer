# 11. Frontend Components

### 🎨 UI Architecture Overview

The CSV Chunker Pro frontend is built as a single-page application using vanilla HTML, CSS, and JavaScript with a component-based approach:

```
App Container
├── Sidebar (Processing Pipeline + Stats)
└── Main Content
    ├── Layer Selection
    ├── File Upload Area  
    ├── Configuration Sections
    ├── Action Buttons
    ├── Download Section (Dynamic)
    └── Search Section (Dynamic)
```

### 🏗️ HTML Structure Breakdown

#### **Root Container**
```html
<div class="app-container">
    <!-- Main application wrapper -->
</div>
```

**Purpose**: Top-level container with flexbox layout
**CSS Classes**: `.app-container`
**Responsive**: Switches to column layout on mobile

#### **Sidebar Component**
```html
<div class="sidebar">
    <div class="sidebar-header">
        <h1>CSV Chunking Optimizer Pro</h1>
    </div>
    
    <div class="processing-pipeline">
        <!-- 6 processing steps -->
    </div>
    
    <div class="stats-section">
        <!-- Processing statistics -->
    </div>
</div>
```

**Key Elements**:
- **Header**: Application title and branding
- **Pipeline**: 6-step processing visualization
- **Stats**: Real-time processing metrics

**JavaScript Interactions**:
- Progress step updates
- Timer management
- Status text changes

#### **Main Content Area**
```html
<div class="main-content">
    <div class="content-section active" id="layer-1-content">
        <!-- Layer 1 content -->
    </div>
    <div class="content-section" id="layer-2-content">
        <!-- Layer 2 content -->
    </div>
    <div class="content-section" id="layer-3-content">
        <!-- Layer 3 content -->
    </div>
</div>
```

**Dynamic Sections**:
- Layer-specific content switching
- Configuration panels
- Generated download/search sections

### 📱 Component Detailed Breakdown

#### **1. Layer Selection Component**
```html
<div class="layer-selector">
    <input type="radio" id="layer-1" name="layer" value="1" checked>
    <label for="layer-1" class="layer-option">
        <div class="layer-icon">⚡</div>
        <div class="layer-content">
            <div class="layer-title">Layer 1 - Fast</div>
            <div class="layer-description">Quick processing with optimized defaults</div>
        </div>
    </label>
    <!-- More layer options... -->
</div>
```

**JavaScript Handler**:
```javascript
function selectLayer(layerNumber) {
    currentLayer = layerNumber;
    
    // Update UI
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`layer-${layerNumber}-content`).classList.add('active');
    
    // Update radio button
    document.getElementById(`layer-${layerNumber}`).checked = true;
    
    console.log(`Layer ${layerNumber} selected`);
}
```

**Features**:
- Radio button selection
- Visual feedback with icons
- Content switching animation
- Keyboard navigation support

#### **2. File Upload Component**
```html
<div class="upload-section">
    <div class="upload-area" id="upload-area">
        <div class="upload-icon">📁</div>
        <div class="upload-text">
            <div class="upload-title">Upload CSV File</div>
            <div class="upload-subtitle">Drag & drop or click to select</div>
        </div>
        <input type="file" id="csv-file" accept=".csv" hidden>
    </div>
    <div class="file-info" id="file-info" style="display: none;">
        <!-- File details display -->
    </div>
</div>
```

**JavaScript Handlers**:
```javascript
// File selection handler
function handleFileUpload(event) {
    const file = event.target.files[0] || event.dataTransfer.files[0];
    
    if (!validateCSVFile(file)) {
        showError("Invalid file type or size");
        return;
    }
    
    displayFileInfo(file);
    currentFile = file;
}

// Drag and drop handlers
function handleDragOver(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload({ target: { files } });
    }
}
```

**Features**:
- Drag & drop support
- File validation (type, size)
- Visual feedback during drag
- File information display
- Error handling

#### **3. Processing Pipeline Component**
```html
<div class="processing-pipeline">
    <div class="process-step" id="step-upload">
        <div class="step-content">
            <div class="step-details">
                <div class="step-title">File Upload</div>
                <div class="step-description">CSV file selection</div>
            </div>
            <div class="step-right-container">
                <span class="step-status-text"></span>
                <span class="step-timing"></span>
                <div class="step-status">📁</div>
            </div>
        </div>
    </div>
    <!-- 5 more steps... -->
</div>
```

**JavaScript Management**:
```javascript
// Step state management
function updateStepStatus(stepId, status) {
    const step = document.getElementById(stepId);
    
    // Remove all status classes
    step.classList.remove('pending', 'active', 'completed', 'error');
    
    // Add new status
    step.classList.add(status);
    
    // Update icon based on status
    const statusElement = step.querySelector('.step-status');
    switch(status) {
        case 'active':
            statusElement.innerHTML = '🔄';
            break;
        case 'completed':
            statusElement.innerHTML = '✅';
            break;
        case 'error':
            statusElement.innerHTML = '❌';
            break;
    }
}

// Timer functions for live updates
function startStepTimer(stepId, stepName) {
    const startTime = Date.now();
    
    updateStepStatus(stepId, 'active');
    updateStepStatusText(stepId, 'Processing');
    
    const intervalId = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        updateStepLiveTime(stepId, elapsed);
    }, 1000);
    
    activeTimers.set(stepId, { startTime, intervalId, stepName });
}
```

**Features**:
- Real-time status updates
- Live timing display
- Visual progress indicators
- Status text management
- Responsive layout

#### **4. Configuration Panels**
```html
<div class="config-section">
    <div class="config-card">
        <div class="config-card-header">
            <div class="config-icon">🔧</div>
            <div class="config-title">Preprocessing</div>
        </div>
        <div class="config-card-content">
            <div class="config-row">
                <label class="config-label">Remove Duplicates</label>
                <div class="toggle-switch">
                    <input type="checkbox" id="remove-duplicates" checked>
                    <label for="remove-duplicates" class="toggle-slider"></label>
                </div>
            </div>
            <!-- More config options... -->
        </div>
    </div>
</div>
```

**JavaScript Configuration**:
```javascript
function getLayerConfiguration(layerNumber) {
    const config = {};
    
    // Collect all form inputs for the layer
    const layerContent = document.getElementById(`layer-${layerNumber}-content`);
    const inputs = layerContent.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            config[input.id] = input.checked;
        } else if (input.type === 'number') {
            config[input.id] = parseInt(input.value);
        } else {
            config[input.id] = input.value;
        }
    });
    
    return config;
}
```

**Features**:
- Toggle switches
- Number inputs with validation
- Dropdown selections
- Dynamic configuration loading
- Form state persistence

#### **5. Action Buttons Component**
```html
<div class="action-buttons">
    <button class="btn btn-secondary" onclick="resetConfiguration()">
        <span class="btn-icon">🔄</span>
        <span class="btn-text">Reset</span>
    </button>
    
    <button class="btn btn-secondary" onclick="saveConfiguration()">
        <span class="btn-icon">💾</span>
        <span class="btn-text">Save Config</span>
    </button>
    
    <button class="btn btn-primary" id="start-processing" onclick="startProcessing()">
        <span class="btn-icon">🚀</span>
        <span class="btn-text">Start Processing</span>
    </button>
</div>
```

**JavaScript Actions**:
```javascript
function resetConfiguration() {
    // Reset all form inputs to defaults
    document.querySelectorAll('input, select').forEach(input => {
        if (input.type === 'checkbox') {
            input.checked = input.hasAttribute('checked');
        } else {
            input.value = input.defaultValue;
        }
    });
    
    showSuccess('Configuration reset to defaults');
}

function saveConfiguration() {
    const config = getLayerConfiguration(currentLayer);
    localStorage.setItem('csvChunkerConfig', JSON.stringify(config));
    showSuccess('Configuration saved');
}

async function startProcessing() {
    if (!currentFile) {
        showError('Please select a CSV file first');
        return;
    }
    
    // Disable button during processing
    const button = document.getElementById('start-processing');
    button.disabled = true;
    button.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">Processing...</span>';
    
    try {
        await processDynamicStepByStep(currentFile);
    } catch (error) {
        handleProcessingError(error);
    } finally {
        // Re-enable button
        button.disabled = false;
        button.innerHTML = '<span class="btn-icon">🚀</span><span class="btn-text">Start Processing</span>';
    }
}
```

**Features**:
- Button state management
- Loading indicators
- Configuration persistence
- Error handling
- Accessibility support

#### **6. Dynamic Download Section**
```javascript
function showRealDownloadButtons(downloadLinks) {
    let downloadSection = document.getElementById('download-section');
    
    if (!downloadSection) {
        downloadSection = document.createElement('div');
        downloadSection.id = 'download-section';
        downloadSection.className = 'config-card';
        
        // Dynamic positioning and styling
        downloadSection.style.cssText = `
            margin: -150px auto 15px auto;
            max-width: 800px;
            width: 100%;
            background: #1d2224;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px;
            position: relative;
            z-index: 999;
            height: auto;
            min-height: 100px;
            overflow: visible;
            top: -60px;
        `;
    }
    
    // Create download buttons
    const buttonsHTML = Object.entries(downloadLinks).map(([type, info]) => `
        <button class="btn btn-download" onclick="downloadFile('${info.url}', '${info.filename}')">
            <span class="btn-icon">${getFileIcon(type)}</span>
            <span class="btn-text">${info.filename}</span>
            <span class="file-size">${formatFileSize(info.size_bytes)}</span>
        </button>
    `).join('');
    
    downloadSection.innerHTML = `
        <div class="config-card-header">
            <div class="config-icon">📁</div>
            <div class="config-title">Download Processed Files</div>
        </div>
        <div class="download-buttons" id="download-buttons">
            ${buttonsHTML}
        </div>
    `;
    
    // Insert into DOM at optimal position
    insertDownloadSection(downloadSection);
}
```

**Features**:
- Dynamic creation and positioning
- File type icons
- Size formatting
- Download functionality
- Responsive layout

#### **7. Expandable Search Section**
```javascript
function enableExpandableSearchInterface(processingId) {
    let searchSection = document.getElementById('expandable-search-section');
    
    if (!searchSection) {
        searchSection = document.createElement('div');
        searchSection.id = 'expandable-search-section';
        
        searchSection.innerHTML = `
            <!-- Collapsed Header -->
            <div id="search-header" class="expandable-header" onclick="toggleSearchSection()">
                <div class="header-content">
                    <div class="header-icon">🔍</div>
                    <div class="header-title">Search Retrieved Chunks</div>
                    <div class="header-subtitle">Click to expand search interface</div>
                </div>
                <div class="toggle-icon" id="search-toggle-icon">▼</div>
            </div>
            
            <!-- Expandable Content -->
            <div id="search-content" class="expandable-content" style="display: none;">
                <div class="search-controls">
                    <input type="text" id="expandable-query-input" placeholder="Enter your search query...">
                    <select id="expandable-similarity-metric">
                        <option value="cosine">Cosine</option>
                        <option value="dot">Dot Product</option>
                        <option value="euclidean">Euclidean</option>
                    </select>
                    <input type="number" id="expandable-top-k" value="5" min="1" max="20">
                    <button onclick="performExpandableSearch('${processingId}')">Search</button>
                </div>
                <div id="expandable-search-results" class="search-results"></div>
            </div>
        `;
    }
    
    // Insert after download section
    insertSearchSection(searchSection);
}

function toggleSearchSection() {
    const content = document.getElementById('search-content');
    const toggleIcon = document.getElementById('search-toggle-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggleIcon.textContent = '▲';
    } else {
        content.style.display = 'none';
        toggleIcon.textContent = '▼';
    }
}
```

**Features**:
- Collapsible interface
- Search controls
- Results display
- Keyboard shortcuts
- Smooth animations

### 🎛️ Event Handling System

#### **Global Event Listeners**
```javascript
function initializeApp() {
    // File upload events
    document.getElementById('csv-file').addEventListener('change', handleFileUpload);
    document.getElementById('upload-area').addEventListener('click', () => {
        document.getElementById('csv-file').click();
    });
    
    // Drag and drop events
    const uploadArea = document.getElementById('upload-area');
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Layer selection events
    document.querySelectorAll('input[name="layer"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            selectLayer(parseInt(e.target.value));
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Window events
    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('error', handleGlobalError);
    
    console.log('CSV Chunking Optimizer initialized successfully!');
}
```

#### **Keyboard Shortcuts**
```javascript
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + Enter: Start processing
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        if (currentFile) {
            startProcessing();
        }
    }
    
    // Ctrl/Cmd + R: Reset configuration
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        resetConfiguration();
    }
    
    // Escape: Close modals or cancel operations
    if (event.key === 'Escape') {
        closeModals();
    }
    
    // Enter in search box: Perform search
    if (event.key === 'Enter' && event.target.id === 'expandable-query-input') {
        const processingId = getCurrentProcessingId();
        if (processingId) {
            performExpandableSearch(processingId);
        }
    }
}
```

### 🎨 CSS Component Styling

#### **Responsive Breakpoints**
```css
/* Mobile First Approach */
@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        height: auto;
    }
    
    .main-content {
        padding: 15px;
    }
    
    .layer-selector {
        flex-direction: column;
    }
}

@media (max-width: 480px) {
    .config-row {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .action-buttons {
        flex-direction: column;
        gap: 10px;
    }
    
    .btn {
        width: 100%;
    }
}
```

#### **Animation System**
```css
/* Smooth transitions */
.process-step {
    transition: all 0.3s ease;
}

.process-step.active {
    background: rgba(74, 144, 226, 0.1);
    border-left: 3px solid #4a90e2;
}

.upload-area {
    transition: all 0.2s ease;
}

.upload-area:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.2);
}

.upload-area.dragover {
    background: rgba(74, 144, 226, 0.1);
    border-color: #4a90e2;
    transform: scale(1.02);
}

/* Button animations */
.btn {
    transition: all 0.2s ease;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
```

### 🔧 State Management

#### **Global State Variables**
```javascript
// Application state
let currentLayer = 1;
let currentFile = null;
let currentProcessingId = null;
let apiClient = null;

// UI state
const activeTimers = new Map();
let isProcessing = false;
let searchEnabled = false;

// Configuration state
let layerConfigurations = {
    1: {},  // Layer 1 config
    2: {},  // Layer 2 config
    3: {}   // Layer 3 config
};
```

#### **State Update Functions**
```javascript
function updateApplicationState(newState) {
    Object.assign(window.appState, newState);
    
    // Trigger UI updates based on state changes
    if (newState.hasOwnProperty('isProcessing')) {
        updateProcessingUI(newState.isProcessing);
    }
    
    if (newState.hasOwnProperty('currentFile')) {
        updateFileDisplay(newState.currentFile);
    }
}

function getApplicationState() {
    return {
        currentLayer,
        currentFile: currentFile ? currentFile.name : null,
        currentProcessingId,
        isProcessing,
        searchEnabled,
        activeTimersCount: activeTimers.size
    };
}
```

### 📱 Mobile Responsiveness

#### **Touch Events**
```javascript
// Touch support for mobile devices
function addTouchSupport() {
    // Touch-friendly file upload
    const uploadArea = document.getElementById('upload-area');
    uploadArea.addEventListener('touchstart', handleTouchStart, { passive: true });
    
    // Swipe gestures for layer switching
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipeGesture();
    }, { passive: true });
    
    function handleSwipeGesture() {
        const swipeThreshold = 100;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next layer
                if (currentLayer < 3) selectLayer(currentLayer + 1);
            } else {
                // Swipe right - previous layer
                if (currentLayer > 1) selectLayer(currentLayer - 1);
            }
        }
    }
}
```

#### **Mobile-Optimized Components**
```css
/* Mobile-specific styles */
@media (max-width: 768px) {
    .upload-area {
        min-height: 120px;
        padding: 20px;
    }
    
    .processing-pipeline {
        padding: 10px;
    }
    
    .process-step {
        padding: 12px;
        margin: 6px 0;
    }
    
    .btn {
        min-height: 44px;  /* iOS touch target size */
        padding: 12px 20px;
    }
    
    .config-card {
        margin: 10px 0;
        padding: 15px;
    }
}
```

This comprehensive frontend documentation covers all UI components, their interactions, styling, and responsive behavior in the CSV Chunker Pro application.

---