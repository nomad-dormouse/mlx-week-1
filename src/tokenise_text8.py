#!/usr/bin/env python
# Tokenise the text8 dataset

import os
import argparse
import pickle
from collections import Counter
import numpy as np

# Fix import issue by using relative import path
try:
    from src.config import (
        TEXT8_DATASET_PATH, TOKENIZED_DATA_DIR, TOKENIZER_PATH, TOKENIZED_TEXT8_PATH,
        VOCAB_SIZE, DEFAULT_CHUNK_SIZE, SPECIAL_TOKENS, PUNCTUATION_MAP,
        ensure_directories
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        TEXT8_DATASET_PATH, TOKENIZED_DATA_DIR, TOKENIZER_PATH, TOKENIZED_TEXT8_PATH,
        VOCAB_SIZE, DEFAULT_CHUNK_SIZE, SPECIAL_TOKENS, PUNCTUATION_MAP,
        ensure_directories
    )

class Tokenizer:
    """
    A simple tokenizer that handles:
    - lowercasing
    - replacing punctuation with special tokens
    - removing whitespace
    - converting tokens to ids
    """
    def __init__(self, vocab_size=VOCAB_SIZE):
        self.vocab_size = vocab_size
        self.word_to_id = {}
        self.id_to_word = {}
        self.special_tokens = SPECIAL_TOKENS
        self.punctuation_map = PUNCTUATION_MAP
    
    def build_vocab(self, text):
        """Build vocabulary from tokenized text."""
        # Preprocess the text
        processed_text = self._preprocess_text(text)
        
        # Split into words and count occurrences
        words = processed_text.split()
        word_counts = Counter(words)
        
        # Add special tokens first
        for token, idx in self.special_tokens.items():
            self.word_to_id[token] = idx
            self.id_to_word[idx] = token
        
        # Add most common words
        idx = len(self.special_tokens)
        for word, _ in word_counts.most_common(self.vocab_size - len(self.special_tokens)):
            if word not in self.word_to_id:
                self.word_to_id[word] = idx
                self.id_to_word[idx] = word
                idx += 1
                
        print(f"Vocabulary built with {len(self.word_to_id)} tokens")
        return self
    
    def _preprocess_text(self, text):
        """Preprocess text for tokenization."""
        # text8 is already lowercase and without punctuation, 
        # but we'll handle it anyway for completeness
        text = text.lower()
        
        # Replace punctuation with special tokens if needed
        for punct, token in self.punctuation_map.items():
            text = text.replace(punct, f" {token} ")
        
        return text
    
    def text_to_ids(self, text):
        """Convert text to a list of token ids."""
        processed_text = self._preprocess_text(text)
        words = processed_text.split()
        
        # Convert words to ids
        ids = []
        for word in words:
            if word in self.word_to_id:
                ids.append(self.word_to_id[word])
            else:
                ids.append(self.special_tokens["<UNK>"])
        
        return ids
    
    def ids_to_text(self, ids):
        """Convert a list of token ids back to text."""
        words = []
        for idx in ids:
            if idx in self.id_to_word:
                word = self.id_to_word[idx]
                # Handle special tokens
                if word in self.special_tokens.keys():
                    for punct, token in self.punctuation_map.items():
                        if token == word:
                            word = punct
                            break
                words.append(word)
            else:
                words.append("<UNK>")
        
        return " ".join(words)
    
    def save(self, output_path):
        """Save the tokenizer to a file."""
        tokenizer_data = {
            'vocab_size': self.vocab_size,
            'word_to_id': self.word_to_id,
            'id_to_word': self.id_to_word,
            'special_tokens': self.special_tokens,
            'punctuation_map': self.punctuation_map
        }
        
        with open(output_path, 'wb') as f:
            pickle.dump(tokenizer_data, f)
        
        print(f"Tokenizer saved to {output_path}")
    
    @classmethod
    def load(cls, input_path):
        """Load a tokenizer from a file."""
        with open(input_path, 'rb') as f:
            tokenizer_data = pickle.load(f)
        
        tokenizer = cls(tokenizer_data['vocab_size'])
        tokenizer.word_to_id = tokenizer_data['word_to_id']
        tokenizer.id_to_word = tokenizer_data['id_to_word']
        tokenizer.special_tokens = tokenizer_data['special_tokens']
        tokenizer.punctuation_map = tokenizer_data['punctuation_map']
        
        print(f"Tokenizer loaded from {input_path}")
        return tokenizer

def tokenise_text8(data_path=TEXT8_DATASET_PATH, output_dir=TOKENIZED_DATA_DIR, 
                  vocab_size=VOCAB_SIZE, chunk_size=DEFAULT_CHUNK_SIZE):
    """
    Tokenize the text8 dataset.
    
    Args:
        data_path (str): Path to the text8 file
        output_dir (str): Directory to save tokenizer and tokenized data
        vocab_size (int): Size of vocabulary
        chunk_size (int): Size of chunks for breaking up the data
    """
    if not os.path.exists(data_path):
        print(f"Error: File not found at {data_path}")
        return
    
    # Ensure directories exist
    ensure_directories()
    
    tokenizer_path = os.path.join(output_dir, "tokenizer.pkl")
    tokens_path = os.path.join(output_dir, "tokenized_text8.npy")
    
    # Read the file
    print(f"Reading text8 dataset from {data_path}...")
    with open(data_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create and train tokenizer
    print(f"Building vocabulary with size {vocab_size}...")
    tokenizer = Tokenizer(vocab_size)
    tokenizer.build_vocab(text)
    
    # Save tokenizer
    tokenizer.save(tokenizer_path)
    
    # Tokenize the entire text
    print("Tokenizing text...")
    token_ids = tokenizer.text_to_ids(text)
    
    # Save as numpy array for easy loading
    print(f"Saving {len(token_ids)} tokens to {tokens_path}...")
    np.save(tokens_path, token_ids)
    
    # Print stats
    print(f"Total tokens: {len(token_ids)}")
    print(f"Unique tokens in vocabulary: {len(tokenizer.word_to_id)}")
    
    # Example: Reconstruct a small part of text to verify
    sample_size = min(100, len(token_ids))
    sample_ids = token_ids[:sample_size]
    reconstructed = tokenizer.ids_to_text(sample_ids)
    
    print("\nSample tokenization:")
    print("Original text (first 100 chars):", text[:100])
    print("Reconstructed from tokens:", reconstructed)
    
    return tokenizer, token_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tokenize the text8 dataset")
    parser.add_argument("--data_path", type=str, default=TEXT8_DATASET_PATH, 
                       help="Path to the text8 file")
    parser.add_argument("--output_dir", type=str, default=TOKENIZED_DATA_DIR, 
                       help="Directory to save tokenizer and tokenized data")
    parser.add_argument("--vocab_size", type=int, default=VOCAB_SIZE,
                       help="Size of vocabulary")
    parser.add_argument("--chunk_size", type=int, default=DEFAULT_CHUNK_SIZE,
                       help="Size of chunks for breaking up the data")
    
    args = parser.parse_args()
    tokenise_text8(args.data_path, args.output_dir, args.vocab_size, args.chunk_size) 