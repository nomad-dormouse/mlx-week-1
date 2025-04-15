#!/usr/bin/env python
# Check the tokenisation of the text8 dataset

import os
import argparse
import pickle
import numpy as np

# Fix import issue by using relative import path
try:
    from src.config import (
        TOKENIZER_PATH, TOKENIZED_TEXT8_PATH, UNK_TOKEN
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        TOKENIZER_PATH, TOKENIZED_TEXT8_PATH, UNK_TOKEN
    )

def load_tokenizer(tokenizer_path):
    """Load a tokenizer from a file."""
    with open(tokenizer_path, 'rb') as f:
        tokenizer_data = pickle.load(f)
    
    print(f"Tokenizer loaded from {tokenizer_path}")
    return tokenizer_data

def check_tokenisation(tokenizer_path=TOKENIZER_PATH, tokens_path=TOKENIZED_TEXT8_PATH, sample_words=None):
    """
    Check and explore the tokenisation results.
    
    Args:
        tokenizer_path (str): Path to the saved tokenizer
        tokens_path (str): Path to the tokenized data
        sample_words (list): List of words to check in the vocabulary
    """
    if not os.path.exists(tokenizer_path):
        print(f"Error: Tokenizer not found at {tokenizer_path}")
        return
    
    if not os.path.exists(tokens_path):
        print(f"Error: Tokenized data not found at {tokens_path}")
        return
    
    # Load the tokenizer
    tokenizer_data = load_tokenizer(tokenizer_path)
    word_to_id = tokenizer_data['word_to_id']
    id_to_word = tokenizer_data['id_to_word']
    special_tokens = tokenizer_data['special_tokens']
    
    # Load the tokenized data
    tokens = np.load(tokens_path)
    
    print(f"Loaded {len(tokens)} tokens from {tokens_path}")
    print(f"Vocabulary size: {len(word_to_id)}")
    
    # Print id_to_word key types to debug
    print("\nPrinting first few id_to_word entries to debug:")
    for i, (key, value) in enumerate(id_to_word.items()):
        print(f"Key type: {type(key)}, Key: {key}, Value: {value}")
        if i >= 5:  # Just show a few examples
            break
    
    # Show special tokens
    print("\nSpecial tokens:")
    for token, idx in special_tokens.items():
        print(f"{token}: {idx}")
    
    # Check sample words in vocabulary
    if sample_words is None:
        sample_words = ["the", "of", "and", "one", "in", "a", "to", "is", 
                       "anarchism", "political", "revolution", "english", "french"]
    
    print("\nSample words in vocabulary:")
    for word in sample_words:
        if word in word_to_id:
            print(f"{word}: {word_to_id[word]}")
        else:
            print(f"{word}: Not in vocabulary (would be mapped to <UNK>: {special_tokens[UNK_TOKEN]})")
    
    # Check token frequency
    print("\nToken frequency (sample):")
    token_counts = {}
    for token_id in tokens[:1000]:  # Check first 1000 tokens
        token_id = int(token_id)  # Make sure it's an integer
        if token_id in token_counts:
            token_counts[token_id] += 1
        else:
            token_counts[token_id] = 1
    
    for token_id, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        word = id_to_word.get(token_id, "<Unknown>")
        print(f"{word} (ID: {token_id}): {count} occurrences")
    
    # Reconstruct a sample of text
    sample_size = min(200, len(tokens))
    sample_ids = tokens[:sample_size]
    
    # Simple reconstruction for demonstration
    reconstructed_words = []
    for idx in sample_ids:
        idx = int(idx)  # Convert to integer
        if idx in id_to_word:
            reconstructed_words.append(id_to_word[idx])
        else:
            reconstructed_words.append(UNK_TOKEN)
    
    print("\nSample reconstruction (first 200 tokens):")
    print(" ".join(reconstructed_words))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check tokenisation of the text8 dataset")
    parser.add_argument("--tokenizer_path", type=str, default=TOKENIZER_PATH, 
                       help="Path to the saved tokenizer")
    parser.add_argument("--tokens_path", type=str, default=TOKENIZED_TEXT8_PATH, 
                       help="Path to the tokenized data")
    
    args = parser.parse_args()
    check_tokenisation(args.tokenizer_path, args.tokens_path) 