#!/usr/bin/env python
# Explore the text8 dataset

import os
import argparse
from collections import Counter

# Fix import issue by using relative import path
try:
    from src.config import (
        TEXT8_DATASET_PATH
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        TEXT8_DATASET_PATH
    )

def explore_text8(data_path, preview_chars=1000, vocab_size=100):
    """
    Explore the text8 dataset with basic statistics and content preview.
    
    Args:
        data_path (str): Path to the text8 file
        preview_chars (int): Number of characters to preview
        vocab_size (int): Number of most common words to display
    """
    if not os.path.exists(data_path):
        print(f"Error: File not found at {data_path}")
        return
    
    # Get file size
    size_mb = os.path.getsize(data_path) / (1024 * 1024)
    print(f"Dataset size: {size_mb:.2f} MB")
    
    # Read the file
    with open(data_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Basic statistics
    total_chars = len(text)
    words = text.split()
    total_words = len(words)
    unique_words = len(set(words))
    
    print(f"Total characters: {total_chars:,}")
    print(f"Total words: {total_words:,}")
    print(f"Unique words: {unique_words:,}")
    print(f"Vocabulary size as percentage of total words: {unique_words/total_words*100:.2f}%")
    
    # Preview the beginning of the text
    print("\nPreview of the first", preview_chars, "characters:")
    print("-" * 50)
    print(text[:preview_chars])
    print("-" * 50)
    
    # Most common words
    print(f"\nTop {vocab_size} most common words:")
    word_counts = Counter(words)
    for word, count in word_counts.most_common(vocab_size):
        print(f"{word}: {count:,}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explore the text8 dataset")
    parser.add_argument("--data_path", type=str, default=TEXT8_DATASET_PATH, 
                        help="Path to the text8 file")
    parser.add_argument("--preview_chars", type=int, default=1000,
                        help="Number of characters to preview")
    parser.add_argument("--vocab_size", type=int, default=20,
                        help="Number of most common words to display")
    
    args = parser.parse_args()
    explore_text8(args.data_path, args.preview_chars, args.vocab_size) 