"""
Fixed preprocessing module for CSV Chunking Optimizer Pro.
Based on your original preprocessor.txt with fixes and improvements.
"""

import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from datetime import datetime
import warnings
from typing import Dict, Any, Optional, Union, Tuple, List

# Import dependencies with fallbacks
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except (ImportError, OSError):
    nlp = None
    SPACY_AVAILABLE = False
    warnings.warn("spaCy not available, text processing will be limited")

try:
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    import nltk
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)
    
    try:
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    except:
        pass
    
    stemmer = PorterStemmer()
    NLTK_AVAILABLE = True
except ImportError:
    stemmer = None
    NLTK_AVAILABLE = False
    warnings.warn("NLTK not available, stemming will be limited")

try:
    import chardet
    CHARDET_AVAILABLE = True
except ImportError:
    CHARDET_AVAILABLE = False
    warnings.warn("chardet not available, encoding detection will be limited")

def _load_csv(input_obj: Union[str, pd.DataFrame, Any]) -> pd.DataFrame:
    """
    Load CSV data from various input types
    
    Args:
        input_obj: CSV file path, DataFrame, or file-like object
        
    Returns:
        pandas DataFrame
    """
    if isinstance(input_obj, pd.DataFrame):
        return input_obj.copy()
    
    if hasattr(input_obj, "read"):
        # File-like object
        try:
            return pd.read_csv(input_obj, engine="python")
        except Exception:
            input_obj.seek(0)
            return pd.read_csv(input_obj)
    
    if isinstance(input_obj, str):
        # File path
        try:
            return pd.read_csv(input_obj, engine="python")
        except Exception:
            if CHARDET_AVAILABLE:
                # Try with encoding detection
                with open(input_obj, "rb") as fh:
                    raw = fh.read()
                enc = chardet.detect(raw).get("encoding", "utf-8")
                return pd.read_csv(input_obj, encoding=enc, engine="python")
            else:
                # Fallback: read first 100 bytes to detect encoding
                with open(input_obj, "rb") as fh:
                    raw = fh.read(100)
                text = raw.decode("utf-8", errors="replace")
                from io import StringIO
                return pd.read_csv(StringIO(text))
    
    raise ValueError("Unsupported input type for _load_csv")

def remove_html(text: str) -> str:
    """
    Remove HTML tags from text
    
    Args:
        text: Input text that may contain HTML
        
    Returns:
        Text with HTML tags removed
    """
    if not isinstance(text, str):
        return text
    
    try:
        return BeautifulSoup(text, "lxml").get_text(separator=' ')
    except:
        # Fallback to regex-based HTML removal
        return re.sub('<[^<]+?>', ' ', text)

def validate_and_normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and normalize DataFrame column headers
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with normalized headers
    """
    new_columns = []
    for i, col in enumerate(df.columns):
        if pd.isna(col) or str(col).strip() == "":
            new_col = f"column_{i+1}"
        else:
            new_col = str(col).strip().lower()
        new_columns.append(new_col)
    
    df.columns = new_columns
    return df

def normalize_text_column(s: pd.Series, 
                         lowercase: bool = True, 
                         strip: bool = True, 
                         remove_html_flag: bool = True) -> pd.Series:
    """
    Normalize text in a pandas Series
    
    Args:
        s: Input pandas Series
        lowercase: Convert to lowercase
        strip: Strip whitespace
        remove_html_flag: Remove HTML tags
        
    Returns:
        Normalized pandas Series
    """
    # Fill NaN values with empty string
    s = s.fillna('')
    
    # Remove HTML if requested
    if remove_html_flag:
        s = s.map(remove_html)
    
    # Convert to lowercase
    if lowercase:
        s = s.map(lambda x: x.lower() if isinstance(x, str) else x)
    
    # Strip whitespace
    if strip:
        s = s.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Normalize multiple spaces to single space
    s = s.map(lambda x: re.sub(r'\s+', ' ', x) if isinstance(x, str) else x)
    
    return s

def apply_type_conversion(df: pd.DataFrame, conversion: Dict[str, str]) -> pd.DataFrame:
    """
    Apply data type conversions to DataFrame columns
    
    Args:
        df: Input DataFrame
        conversion: Dictionary mapping column names to target types
        
    Returns:
        DataFrame with converted types
    """
    df = df.copy()
    
    for col, target_type in conversion.items():
        if col not in df.columns:
            warnings.warn(f"Column '{col}' not found in DataFrame")
            continue
        
        try:
            if target_type == 'numeric':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif target_type == 'datetime':
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif target_type == 'text' or target_type == 'string':
                df[col] = df[col].astype(str)
            elif target_type == 'bool' or target_type == 'boolean':
                # Convert to boolean, handling various formats
                df[col] = df[col].map(lambda x: str(x).lower() in ['true', '1', 'yes', 'on'] if pd.notna(x) else False)
            else:
                warnings.warn(f"Unknown type conversion: {target_type}")
        except Exception as e:
            warnings.warn(f"Failed to convert column '{col}' to {target_type}: {e}")
    
    return df

def remove_stopwords_from_text_column(df: pd.DataFrame, remove_stopwords: bool = True) -> pd.DataFrame:
    """
    Remove stopwords from text columns in DataFrame
    
    Args:
        df: Input DataFrame
        remove_stopwords: Whether to remove stopwords
        
    Returns:
        DataFrame with stopwords removed from text columns
    """
    if not remove_stopwords or not SPACY_AVAILABLE:
        return df
    
    # Detect text/object columns with text content
    text_cols = []
    for col in df.select_dtypes(include=["object"]).columns:
        # Check if column contains text (not just numbers/dates)
        sample_values = df[col].dropna().astype(str).head(100)
        if sample_values.str.match(r'.*[a-zA-Z]+.*').any():
            text_cols.append(col)
    
    if not text_cols:
        return df  # No text columns found
    
    def process_text(text):
        """Process individual text to remove stopwords"""
        if pd.isna(text) or text == '':
            return text
        
        try:
            doc = nlp(str(text))
            filtered_tokens = [token.text for token in doc if not token.is_stop and token.text.strip()]
            return " ".join(filtered_tokens)
        except Exception:
            return str(text)  # Return original if processing fails
    
    # Apply stopword removal to detected text columns
    for col in text_cols:
        df[col] = df[col].apply(process_text)
    
    return df

def lemmatize_text(text: str) -> str:
    """
    Lemmatize text using spaCy
    
    Args:
        text: Input text
        
    Returns:
        Lemmatized text
    """
    if not SPACY_AVAILABLE or pd.isna(text):
        return str(text)
    
    try:
        doc = nlp(str(text))
        return " ".join([token.text if token.lemma_ == '-PRON-' else token.lemma_ for token in doc])
    except Exception:
        return str(text)

def stem_text(text: str) -> str:
    """
    Stem text using NLTK Porter Stemmer
    
    Args:
        text: Input text
        
    Returns:
        Stemmed text
    """
    if not NLTK_AVAILABLE or pd.isna(text):
        return str(text)
    
    try:
        words = word_tokenize(str(text))
        return " ".join([stemmer.stem(word) for word in words])
    except Exception:
        return str(text)

def process_text(df: pd.DataFrame, method: str) -> pd.DataFrame:
    """
    Apply text processing to DataFrame
    
    Args:
        df: Input DataFrame
        method: Processing method ('lemmatize', 'stem', or 'skip')
        
    Returns:
        DataFrame with processed text
    """
    if method == 'skip':
        return df
    
    # Find text columns
    text_cols = df.select_dtypes(include=["object"]).columns
    
    for col in text_cols:
        if method == 'lemmatize':
            df[col] = df[col].apply(lemmatize_text)
        elif method == 'stem':
            df[col] = df[col].apply(stem_text)
        else:
            warnings.warn(f"Unknown text processing method: {method}")
    
    return df

def handle_null_values(df: pd.DataFrame, null_handling: Dict[str, Any]) -> pd.DataFrame:
    """
    Handle null values according to specified strategies
    
    Args:
        df: Input DataFrame
        null_handling: Dictionary specifying null handling strategy per column
        
    Returns:
        DataFrame with null values handled
    """
    df = df.copy()
    
    for col, strategy in null_handling.items():
        if col not in df.columns:
            warnings.warn(f"Column '{col}' not found in DataFrame")
            continue
        
        # Handle both string strategies and dict strategies
        if isinstance(strategy, dict):
            strategy_name = strategy.get('strategy', 'skip')
            custom_value = strategy.get('value', None)
        else:
            strategy_name = strategy
            custom_value = None
        
        try:
            if strategy_name == 'skip' or strategy_name == 'leave_as_is':
                continue
            elif strategy_name == 'drop':
                df = df.dropna(subset=[col])
            elif strategy_name == 'mean':
                if df[col].dtype in ['int64', 'float64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    warnings.warn(f"Cannot compute mean for non-numeric column '{col}'")
            elif strategy_name == 'median':
                if df[col].dtype in ['int64', 'float64']:
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    warnings.warn(f"Cannot compute median for non-numeric column '{col}'")
            elif strategy_name == 'mode':
                mode_value = df[col].mode()
                if len(mode_value) > 0:
                    df[col].fillna(mode_value.iloc[0], inplace=True)
            elif strategy_name == 'custom':
                if custom_value is not None:
                    df[col].fillna(custom_value, inplace=True)
                else:
                    warnings.warn(f"Custom value not provided for column '{col}'")
            else:
                warnings.warn(f"Unknown null handling strategy: {strategy_name}")
        except Exception as e:
            warnings.warn(f"Failed to handle nulls in column '{col}': {e}")
    
    return df

def preprocess_csv(input_obj: Union[str, pd.DataFrame, Any],
                  preprocessing_config: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
    """
    Comprehensive CSV preprocessing function
    
    Args:
        input_obj: CSV file path, DataFrame, or file-like object
        preprocessing_config: Configuration dictionary for preprocessing steps
        
    Returns:
        Tuple of (processed_dataframe, file_metadata, numeric_metadata)
    """
    # Set default configuration
    if preprocessing_config is None:
        preprocessing_config = {}
    
    # Load CSV data
    df = _load_csv(input_obj)
    
    # Validate and normalize headers
    df = validate_and_normalize_headers(df)
    
    # Normalize text columns (object dtype)
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in text_cols:
        df[col] = normalize_text_column(df[col])
    
    # Apply type conversions
    type_conversions = preprocessing_config.get('type_conversions', {})
    if type_conversions:
        df = apply_type_conversion(df, type_conversions)
    
    # Handle null values
    null_handling = preprocessing_config.get('null_handling', {})
    if null_handling:
        df = handle_null_values(df, null_handling)
    
    # Drop duplicates if requested
    if preprocessing_config.get('remove_duplicates', False):
        initial_count = len(df)
        df = df.drop_duplicates(keep='first')
        final_count = len(df)
        if initial_count != final_count:
            print(f"Removed {initial_count - final_count} duplicate rows")
    
    # Remove stopwords if requested
    if preprocessing_config.get('remove_stopwords', False):
        df = remove_stopwords_from_text_column(df, remove_stopwords=True)
    
    # Apply text processing
    text_processing = preprocessing_config.get('text_processing', 'skip')
    df = process_text(df, text_processing)
    
    # Prepare file metadata
    file_meta = {
        'file_source': input_obj if isinstance(input_obj, str) else 'dataframe_input',
        'num_rows': df.shape[0],
        'num_columns': df.shape[1],
        'shape': df.shape,
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.astype(str).to_dict(),
        'upload_time': datetime.utcnow().isoformat() + 'Z',
        'preprocessing_config': preprocessing_config
    }
    
    # Prepare numeric metadata
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_metadata = []
    
    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) > 0:
            numeric_metadata.append({
                'column_name': col,
                'count': int(col_data.count()),
                'mean': float(col_data.mean()),
                'std': float(col_data.std()) if len(col_data) > 1 else 0.0,
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'median': float(col_data.median()),
                'null_count': int(df[col].isnull().sum()),
                'data_type': str(df[col].dtype)
            })
    
    return df, file_meta, numeric_metadata

# Legacy function for backward compatibility
def preprocess_csv_legacy(input_obj, 
                         fill_null_strategy=None, 
                         type_conversions=None, 
                         drop_duplicates_cols=None, 
                         remove_stopwords_flag=False):
    """
    Legacy preprocessing function for backward compatibility
    """
    # Convert old parameters to new config format
    preprocessing_config = {
        'remove_duplicates': bool(drop_duplicates_cols),
        'remove_stopwords': remove_stopwords_flag,
        'text_processing': 'skip'
    }
    
    if type_conversions:
        preprocessing_config['type_conversions'] = type_conversions
    
    return preprocess_csv(input_obj, preprocessing_config)
