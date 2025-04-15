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

# Hacker News variables
HACKER_NEWS_DATASET_PATH = os.getenv("HACKER_NEWS_DATASET_PATH", "data/hacker_news_complete.csv")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "postgresql://user:password@host:port/database")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "20000"))

# Tokenization variables
TOKENIZED_DATA_DIR = os.getenv("TOKENIZED_DATA_DIR", "data/tokenized")
TOKENIZER_PATH = os.getenv("TOKENIZER_PATH", "data/tokenized/tokenizer.pkl")
TOKENIZED_TEXT8_PATH = os.getenv("TOKENIZED_TEXT8_PATH", "data/tokenized/tokenized_text8.npy")
VOCAB_SIZE = int(os.getenv("VOCAB_SIZE", "10000"))
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000000"))

# Special tokens
PAD_TOKEN = os.getenv("PAD_TOKEN", "<PAD>")
UNK_TOKEN = os.getenv("UNK_TOKEN", "<UNK>")
COMMA_TOKEN = os.getenv("COMMA_TOKEN", "<COMMA>")
PERIOD_TOKEN = os.getenv("PERIOD_TOKEN", "<PERIOD>")
EXCLAMATION_TOKEN = os.getenv("EXCLAMATION_TOKEN", "<EXCLAMATION>")
QUESTION_TOKEN = os.getenv("QUESTION_TOKEN", "<QUESTION>")
SEMICOLON_TOKEN = os.getenv("SEMICOLON_TOKEN", "<SEMICOLON>")
COLON_TOKEN = os.getenv("COLON_TOKEN", "<COLON>")
HYPHEN_TOKEN = os.getenv("HYPHEN_TOKEN", "<HYPHEN>")
QUOTE_TOKEN = os.getenv("QUOTE_TOKEN", "<QUOTE>")

# Create a dictionary of special tokens for easy access
SPECIAL_TOKENS = {
    PAD_TOKEN: 0,
    UNK_TOKEN: 1,
    COMMA_TOKEN: 2,
    PERIOD_TOKEN: 3,
    EXCLAMATION_TOKEN: 4,
    QUESTION_TOKEN: 5,
    SEMICOLON_TOKEN: 6,
    COLON_TOKEN: 7,
    HYPHEN_TOKEN: 8,
    QUOTE_TOKEN: 9,
}

# Create a punctuation mapping
PUNCTUATION_MAP = {
    ",": COMMA_TOKEN,
    ".": PERIOD_TOKEN,
    "!": EXCLAMATION_TOKEN,
    "?": QUESTION_TOKEN,
    ";": SEMICOLON_TOKEN,
    ":": COLON_TOKEN,
    "-": HYPHEN_TOKEN,
    '"': QUOTE_TOKEN,
    "'": QUOTE_TOKEN,
}

# Ensure directories exist
def ensure_directories():
    """Ensure required directories exist"""
    pathlib.Path(DATA_DIR).mkdir(exist_ok=True)
    pathlib.Path(TOKENIZED_DATA_DIR).mkdir(exist_ok=True)

# Call ensure_directories if this script is run directly
if __name__ == "__main__":
    ensure_directories()
    print("Configuration loaded from .env file:")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"TEXT8_DATASET_PATH: {TEXT8_DATASET_PATH}")
    print(f"HACKER_NEWS_DATASET_PATH: {HACKER_NEWS_DATASET_PATH}")
    print(f"TOKENIZED_DATA_DIR: {TOKENIZED_DATA_DIR}")
    print(f"VOCAB_SIZE: {VOCAB_SIZE}")
    print(f"Special tokens: {list(SPECIAL_TOKENS.keys())}") 