#!/usr/bin/env python
# Load configuration from .env file

import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file
load_dotenv()

# Path variables
DATA_DIR = os.getenv("DATA_DIR", "data")
TEXT8_DATASET_PATH = os.getenv("TEXT8_DATASET_PATH", "data/text8")
TEXT8_DATASET_URL = os.getenv("TEXT8_DATASET_URL", "http://mattmahoney.net/dc/text8.zip")
HACKER_NEWS_DATASET_PATH = os.getenv("HACKER_NEWS_DATASET_PATH", "data/hacker_news_complete.csv")
HACKER_NEWS_TITLES_PATH = os.getenv("HACKER_NEWS_TITLES_PATH", "data/hacker_news_titles.txt")
COMBINED_DATASET_PATH = os.getenv("COMBINED_DATASET_PATH", "data/combined_data.txt")
TOKENS_PATH = os.getenv("TOKENS_PATH", "data/tokens.txt")
VOCAB_PATH = os.getenv("VOCAB_PATH", "data/vocab.json")

# Processing parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "50000"))
MAX_VOCAB_SIZE = int(os.getenv("MAX_VOCAB_SIZE", "50000"))

# Ensure directories exist
def ensure_directories():
    """Ensure required directories exist"""
    pathlib.Path(DATA_DIR).mkdir(exist_ok=True)

# Call ensure_directories if this script is run directly
if __name__ == "__main__":
    ensure_directories()
    print("Configuration loaded from .env file:")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"TEXT8_DATASET_PATH: {TEXT8_DATASET_PATH}")
    print(f"TEXT8_DATASET_URL: {TEXT8_DATASET_URL}")
    print(f"HACKER_NEWS_DATASET_PATH: {HACKER_NEWS_DATASET_PATH}")
    print(f"HACKER_NEWS_TITLES_PATH: {HACKER_NEWS_TITLES_PATH}")
    print(f"COMBINED_DATASET_PATH: {COMBINED_DATASET_PATH}")
    print(f"TOKENS_PATH: {TOKENS_PATH}")
    print(f"VOCAB_PATH: {VOCAB_PATH}")
    print(f"CHUNK_SIZE: {CHUNK_SIZE}")
    print(f"MAX_VOCAB_SIZE: {MAX_VOCAB_SIZE}") 