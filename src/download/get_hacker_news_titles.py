#!/usr/bin/env python
# Extract and concatenate titles from the Hacker News dataset

import os
import pandas as pd
import re
import string

# Fix import issue by using relative import path
try:
    from src.config import (
        DATA_DIR, HACKER_NEWS_DATASET_PATH, HACKER_NEWS_TITLES_PATH, 
        CHUNK_SIZE, ensure_directories
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        DATA_DIR, HACKER_NEWS_DATASET_PATH, HACKER_NEWS_TITLES_PATH, 
        CHUNK_SIZE, ensure_directories
    )

def clean_title(title):
    """Clean and normalize a title string."""
    if not isinstance(title, str):
        return ""
    
    # Convert to lowercase
    title = title.lower()
    
    # Remove URLs
    title = re.sub(r'https?://\S+|www\.\S+', '', title)
    
    # Remove special characters except spaces and alphanumeric chars
    title = re.sub(r'[^\w\s]', ' ', title)
    
    # Replace multiple spaces with a single space
    title = re.sub(r'\s+', ' ', title)
    
    # Strip leading/trailing whitespace
    title = title.strip()
    
    return title

def get_hacker_news_titles():
    """Extract and concatenate titles from the Hacker News dataset."""
    ensure_directories()
    
    if not os.path.exists(HACKER_NEWS_DATASET_PATH):
        print(f"Error: Hacker News dataset not found at {HACKER_NEWS_DATASET_PATH}")
        return
    
    print(f"Loading Hacker News dataset from {HACKER_NEWS_DATASET_PATH}")
    print(f"Processing in chunks of {CHUNK_SIZE:,} rows")
    
    # Read the CSV file in chunks to handle large files efficiently
    all_titles = []
    total_rows = 0
    
    for chunk in pd.read_csv(HACKER_NEWS_DATASET_PATH, chunksize=CHUNK_SIZE):
        # Filter to keep only rows with a title
        chunk = chunk[chunk['title'].notna()]
        
        # Clean titles
        chunk['clean_title'] = chunk['title'].apply(clean_title)
        
        # Filter out empty titles after cleaning
        chunk = chunk[chunk['clean_title'].str.len() > 0]
        
        all_titles.extend(chunk['clean_title'].tolist())
        total_rows += len(chunk)
        print(f"Processed {total_rows:,} titles so far...")
    
    # Join all titles with spaces
    combined_text = ' '.join(all_titles)
    
    # Save to file
    with open(HACKER_NEWS_TITLES_PATH, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    # Print some statistics
    print(f"\nExtracted {len(all_titles):,} non-empty titles")
    print(f"Total characters: {len(combined_text):,}")
    print(f"Saved concatenated titles to {HACKER_NEWS_TITLES_PATH}")
    
    return HACKER_NEWS_TITLES_PATH

if __name__ == "__main__":
    get_hacker_news_titles() 