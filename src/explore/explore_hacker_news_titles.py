#!/usr/bin/env python
# Explore the Hacker News titles dataset

import os
from collections import Counter

# Fix import issue by using relative import path
try:
    from src.config import HACKER_NEWS_TITLES_PATH
except ModuleNotFoundError:
    # When running as a script directly
    from config import HACKER_NEWS_TITLES_PATH

def explore_hacker_news_titles():
    """Display basic statistics and preview of the Hacker News titles dataset"""
    data_path = HACKER_NEWS_TITLES_PATH
    preview_chars = 500
    vocab_size = 20
    
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
    
    # Count word occurrences
    word_counts = Counter(words)
    
    # Word length distribution
    word_lengths = [len(word) for word in set(words)]
    avg_word_length = sum(word_lengths) / len(word_lengths)
    print(f"\nAverage word length: {avg_word_length:.2f} characters")
    
    # Most common words
    print(f"\nTop {vocab_size} most common words:")
    for word, count in word_counts.most_common(vocab_size):
        print(f"{word}: {count:,}")
    
    # Least common words
    print(f"\nTop {vocab_size} least common words:")
    for word, count in word_counts.most_common()[:-vocab_size-1:-1]:
        print(f"{word}: {count:,}")
    
    # Long words (more than 10 characters)
    long_words = [word for word in set(words) if len(word) > 10]
    print(f"\nSample of long words (>10 chars, {len(long_words)} total):")
    for word in sorted(long_words, key=len, reverse=True)[:10]:
        print(f"{word} ({len(word)} chars): {word_counts[word]:,} occurrences")

if __name__ == "__main__":
    explore_hacker_news_titles() 