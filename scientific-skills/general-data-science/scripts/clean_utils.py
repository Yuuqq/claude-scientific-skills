
import pandas as pd
import numpy as np
from typing import List, Union

def remove_outliers_iqr(df: pd.DataFrame, columns: List[str], factor: float = 1.5) -> pd.DataFrame:
    """
    Remove rows containing outliers in specified columns using Tukey's IQR rules.
    
    Args:
        df: Input DataFrame.
        columns: List of numerical columns to check.
        factor: Multiplier for IQR (1.5 is standard, 3.0 is conservative).
        
    Returns:
        DataFrame with outliers removed.
    """
    mask = pd.Series([True] * len(df), index=df.index)
    
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - (factor * IQR)
        upper_bound = Q3 + (factor * IQR)
        
        col_mask = (df[col] >= lower_bound) & (df[col] <= upper_bound)
        mask = mask & col_mask
        
    print(f"Removed {len(df) - mask.sum()} outlier rows.")
    return df[mask].copy()

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Downcast numerical types and convert objects to categories to save memory.
    """
    # Floats
    fcols = df.select_dtypes('float').columns
    for c in fcols:
        df[c] = pd.to_numeric(df[c], downcast='float')
        
    # Integers
    icols = df.select_dtypes('integer').columns
    for c in icols:
        df[c] = pd.to_numeric(df[c], downcast='integer')
        
    # Objects -> Category (if low cardinality)
    ocols = df.select_dtypes('object').columns
    for c in ocols:
        num_unique = df[c].nunique()
        num_total = len(df)
        if num_unique / num_total < 0.5: # 50% threshold
            df[c] = df[c].astype('category')
            
    return df

def normalize_strings(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Lowercase and strip whitespace from string columns.
    """
    for col in columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
             # Accesor .str works on both object and category (mostly)
             # But for safely, convert to string first if it's object
             df[col] = df[col].astype(str).str.lower().str.strip()
    return df
