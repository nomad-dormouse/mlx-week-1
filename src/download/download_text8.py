#!/usr/bin/env python
# Download the text8 dataset

import os
import urllib.request
import zipfile
import shutil

# Fix import issue by using relative import path
try:
    from src.config import DATA_DIR, TEXT8_DATASET_PATH, TEXT8_DATASET_URL, ensure_directories
except ModuleNotFoundError:
    # When running as a script directly
    from config import DATA_DIR, TEXT8_DATASET_PATH, TEXT8_DATASET_URL, ensure_directories

def download_text8():
    """Download the text8 dataset from the web"""
    ensure_directories()
    
    zip_path = os.path.join(DATA_DIR, "text8.zip")
    original_file = os.path.join(DATA_DIR, "text8")  # File name in the zip archive
    
    # Skip if already downloaded
    if os.path.exists(TEXT8_DATASET_PATH):
        print(f"Dataset already exists at {TEXT8_DATASET_PATH}")
        print(f"Size: {os.path.getsize(TEXT8_DATASET_PATH) / (1024 * 1024):.2f} MB")
        return TEXT8_DATASET_PATH
    
    # Download the zip file
    if not os.path.exists(zip_path):
        print(f"Downloading from {TEXT8_DATASET_URL}...")
        urllib.request.urlretrieve(TEXT8_DATASET_URL, zip_path)
    
    # Extract the zip file
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
    
    # Rename the extracted file to have .txt extension
    if os.path.exists(original_file):
        shutil.move(original_file, TEXT8_DATASET_PATH)
    
    # Clean up
    os.remove(zip_path)
    
    print(f"Dataset downloaded to {TEXT8_DATASET_PATH}")
    print(f"Size: {os.path.getsize(TEXT8_DATASET_PATH) / (1024 * 1024):.2f} MB")
    
    return TEXT8_DATASET_PATH

if __name__ == "__main__":
    download_text8() 