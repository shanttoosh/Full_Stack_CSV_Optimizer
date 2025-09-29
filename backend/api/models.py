"""
Pydantic models for request/response validation
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime

# Base Models
class ProcessingSettings(BaseModel):
    """Base processing settings"""
    preprocessing: Optional[Dict[str, Any]] = None
    chunking: Optional[Dict[str, Any]] = None
    embedding: Optional[Dict[str, Any]] = None
    storage: Optional[Dict[str, Any]] = None

# Request Models
class BaseProcessRequest(BaseModel):
    """Base request for CSV processing"""
    csv_data: str = Field(..., description="Base64 encoded CSV data")
    filename: str = Field(..., description="Original filename")
    
    @validator('filename')
    def validate_filename(cls, v):
        if not v.endswith('.csv'):
            raise ValueError('File must have .csv extension')
        return v

class Layer1ProcessRequest(BaseProcessRequest):
    """Layer 1 (Fast) processing request"""
    pass  # Uses all defaults

class Layer2ProcessRequest(BaseProcessRequest):
    """Layer 2 (Config) processing request"""
    chunking_method: Optional[Literal["fixed", "recursive", "semantic", "document_based"]] = "semantic"
    embedding_model: Optional[Literal["all-MiniLM-L6-v2", "BAAI/bge-small-en-v1.5"]] = "all-MiniLM-L6-v2"
    batch_size: Optional[int] = Field(64, ge=1, le=256)

class Layer3ProcessRequest(BaseProcessRequest):
    """Layer 3 (Deep Config) processing request"""
    preprocessing: Optional[Dict[str, Any]] = None
    chunking: Optional[Dict[str, Any]] = None
    embedding: Optional[Dict[str, Any]] = None
    storage: Optional[Dict[str, Any]] = None

class UnifiedProcessRequest(BaseProcessRequest):
    """Unified API processing request"""
    layer_mode: Literal["fast", "config", "deep"] = "fast"
    preprocessing: Optional[Dict[str, Any]] = None
    chunking: Optional[Dict[str, Any]] = None
    embedding: Optional[Dict[str, Any]] = None
    storage: Optional[Dict[str, Any]] = None

class SearchRequest(BaseModel):
    """Search request"""
    query: str = Field(..., min_length=1, description="Search query")
    model_name: Optional[Literal["all-MiniLM-L6-v2", "BAAI/bge-small-en-v1.5"]] = "all-MiniLM-L6-v2"
    top_k: Optional[int] = Field(5, ge=1, le=100)
    similarity_metric: Optional[Literal["cosine", "dot", "euclidean"]] = "cosine"
    where: Optional[Dict[str, Any]] = None

# Response Models
class DownloadLink(BaseModel):
    """Download link information"""
    url: str
    file_id: str
    expires_at: str
    type: str
    size_bytes: Optional[int] = None

class ProcessingSummary(BaseModel):
    """Processing summary information"""
    processing_id: str
    layer_mode: str
    timestamp: str
    processing_time_seconds: float
    input_data: Dict[str, Any]
    chunking_results: Dict[str, Any]
    embedding_results: Dict[str, Any]
    performance_metrics: Dict[str, Any]

class ProcessResponse(BaseModel):
    """Processing response"""
    success: bool
    processing_id: str
    timestamp: str
    processing_summary: ProcessingSummary
    download_links: Dict[str, DownloadLink]
    search_endpoint: Optional[str] = None
    message: Optional[str] = None

class SearchResponse(BaseModel):
    """Search response"""
    success: bool
    processing_id: str
    query: str
    similarity_metric: str
    total_results: int
    results: List[Dict[str, Any]]
    processing_time_seconds: float

class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    timestamp: str
    processing_id: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

class InfoResponse(BaseModel):
    """API information response"""
    app_name: str
    version: str
    description: str
    available_endpoints: List[str]
    supported_models: List[str]
    supported_chunking_methods: List[str]
    supported_similarity_metrics: List[str]

# Internal Models
class ProcessingJob(BaseModel):
    """Internal processing job model"""
    processing_id: str
    layer_mode: str
    settings: ProcessingSettings
    csv_data: str
    filename: str
    created_at: datetime
    status: Literal["pending", "processing", "completed", "failed"] = "pending"
    error_message: Optional[str] = None

class FileInfo(BaseModel):
    """File information model"""
    file_id: str
    processing_id: str
    file_type: str
    filename: str
    size_bytes: int
    created_at: datetime
    expires_at: datetime
    file_path: str
