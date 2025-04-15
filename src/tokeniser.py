#!/usr/bin/env python
# Combine and tokenize the text8 and Hacker News titles datasets

import os
import json
from collections import Counter

# Fix import issue by using relative import path
try:
    from src.config import (
        DATA_DIR, TEXT8_DATASET_PATH, HACKER_NEWS_TITLES_PATH, 
        COMBINED_DATASET_PATH, TOKENS_PATH, VOCAB_PATH,
        MAX_VOCAB_SIZE, ensure_directories
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        DATA_DIR, TEXT8_DATASET_PATH, HACKER_NEWS_TITLES_PATH, 
        COMBINED_DATASET_PATH, TOKENS_PATH, VOCAB_PATH,
        MAX_VOCAB_SIZE, ensure_directories
    )

def combine_datasets():
    """Combine text8 and Hacker News titles into a single dataset."""
    if not os.path.exists(TEXT8_DATASET_PATH):
        print(f"Error: text8 dataset not found at {TEXT8_DATASET_PATH}")
        return False
    
    if not os.path.exists(HACKER_NEWS_TITLES_PATH):
        print(f"Error: Hacker News titles not found at {HACKER_NEWS_TITLES_PATH}")
        return False
    
    print(f"Combining datasets from {TEXT8_DATASET_PATH} and {HACKER_NEWS_TITLES_PATH}")
    
    # Read the text8 dataset
    with open(TEXT8_DATASET_PATH, 'r', encoding='utf-8') as f:
        text8_data = f.read()
    
    # Read the Hacker News titles
    with open(HACKER_NEWS_TITLES_PATH, 'r', encoding='utf-8') as f:
        hn_data = f.read()
    
    # Combine with a separator
    combined_data = text8_data + " " + hn_data
    
    # Save the combined data
    with open(COMBINED_DATASET_PATH, 'w', encoding='utf-8') as f:
        f.write(combined_data)
    
    print(f"Combined dataset saved to {COMBINED_DATASET_PATH}")
    print(f"Total size: {len(combined_data):,} characters")
    
    return combined_data

def tokenize_and_build_vocab(text):
    """Tokenize the text by whitespace and build vocabulary."""
    print("Tokenizing text and building vocabulary...")
    
    # Split by whitespace
    tokens = text.split()
    print(f"Total tokens: {len(tokens):,}")
    
    # Save all tokens to file
    with open(TOKENS_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(tokens))
    
    print(f"All tokens saved to {TOKENS_PATH}")
    
    # Count frequencies
    token_counts = Counter(tokens)
    print(f"Unique tokens: {len(token_counts):,}")
    
    # Limit vocabulary size to most frequent tokens
    vocab = {}
    for i, (token, count) in enumerate(token_counts.most_common(MAX_VOCAB_SIZE)):
        vocab[token] = {"id": i, "count": count}
    
    print(f"Final vocabulary size: {len(vocab):,}")
    
    # Save vocabulary to file
    with open(VOCAB_PATH, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=2)
    
    print(f"Vocabulary saved to {VOCAB_PATH}")
    
    # Print some statistics
    print("\nVocabulary statistics:")
    counts = [count for token, count in token_counts.most_common(MAX_VOCAB_SIZE)]
    if counts:
        print(f"Most common token frequency: {counts[0]:,}")
        print(f"Least common token frequency in vocab: {counts[-1]:,}")
        print(f"Median token frequency in vocab: {counts[len(counts)//2]:,}")
    
    return vocab

def tokeniser():
    """Main function to combine datasets and tokenize."""
    ensure_directories()
    
    # Combine datasets
    combined_data = combine_datasets()
    if not combined_data:
        return
    
    # Tokenize and build vocabulary
    vocab = tokenize_and_build_vocab(combined_data)
    
    return vocab

if __name__ == "__main__":
    tokeniser() 