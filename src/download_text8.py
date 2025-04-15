#!/usr/bin/env python
# Download the text8 dataset directly from source

import os
import urllib.request
import zipfile
import argparse

# Fix import issue by using relative import path
try:
    from src.config import (
        DATA_DIR, TEXT8_DATASET_PATH, TEXT8_DATASET_URL,
        ensure_directories
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        DATA_DIR, TEXT8_DATASET_PATH, TEXT8_DATASET_URL,
        ensure_directories
    )

def download_text8(output_dir=DATA_DIR):
    """
    Download the text8 dataset and save it to the specified directory.
    
    Args:
        output_dir (str): Directory where the dataset will be saved
    """
    print("Downloading text8 dataset...")
    
    # Ensure directories exist
    ensure_directories()
    
    # URL for the text8 dataset
    url = TEXT8_DATASET_URL
    zip_path = os.path.join(output_dir, "text8.zip")
    extracted_path = TEXT8_DATASET_PATH  # The actual extracted file name
    
    # Download the zip file if it doesn't exist
    if not os.path.exists(extracted_path):
        if not os.path.exists(zip_path):
            print(f"Downloading from {url}...")
            urllib.request.urlretrieve(url, zip_path)
            print(f"Downloaded to {zip_path}")
        
        # Extract the zip file
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Remove the zip file after extraction
        os.remove(zip_path)
        print(f"Removed {zip_path}")
    
    if os.path.exists(extracted_path):
        print(f"Dataset found at {extracted_path}")
        print(f"Size: {os.path.getsize(extracted_path) / (1024 * 1024):.2f} MB")
    else:
        print(f"Error: Could not find the extracted file at {extracted_path}")
    
    return extracted_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download text8 dataset")
    parser.add_argument("--output_dir", type=str, default=DATA_DIR, 
                        help="Directory where the dataset will be saved")
    
    args = parser.parse_args()
    download_text8(args.output_dir) 