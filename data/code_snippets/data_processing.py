# Data Processing Pipeline
# A utility function I frequently use for cleaning and processing data

import pandas as pd
import numpy as np
from typing import List, Dict, Any

def clean_dataframe(df: pd.DataFrame, 
                   drop_duplicates: bool = True,
                   handle_missing: str = 'drop') -> pd.DataFrame:
    """
    A comprehensive data cleaning function that I use in most of my projects.
    
    This reflects my approach to data preprocessing - always start with clean,
    reliable data before any analysis or modeling.
    """
    # Make a copy to avoid modifying original
    cleaned_df = df.copy()
    
    # Remove duplicates if requested
    if drop_duplicates:
        original_rows = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        print(f"Removed {original_rows - len(cleaned_df)} duplicate rows")
    
    # Handle missing values
    if handle_missing == 'drop':
        cleaned_df = cleaned_df.dropna()
    elif handle_missing == 'fill':
        # Fill numeric columns with median, categorical with mode
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype in ['int64', 'float64']:
                cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
            else:
                cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
    
    return cleaned_df

def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Data quality assessment function - I believe in understanding
    your data before making any assumptions.
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    
    return report
