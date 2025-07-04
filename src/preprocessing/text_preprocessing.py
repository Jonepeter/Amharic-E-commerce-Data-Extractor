import os
import pandas as pd
from etnltk import Amharic
from etnltk.lang.am import clean_amharic, normalize
from etnltk.tokenize.am import word_tokenize
import re

RAW_CSV_PATH = '../../data/raw/raw_messages.csv'
PROCESSED_CSV_PATH = '../../data/processed/preprocessed_messages.csv'

def preprocess_amharic_text(text):
    if not isinstance(text, str):
        return '', ''
    # Clean and normalize text using etnltk
    cleaned = clean_amharic(text, keep_numbers=True)
    normalized = normalize(cleaned)
    # Tokenize using etnltk's Amharic word_tokenize
    tokens = word_tokenize(normalized)
    return normalized, ' '.join(tokens)

def preprocess_dataframe(df):
    processed_rows = []
    for _, row in df.iterrows():
        raw_text = row.get('text', '')
        clean, tokens = preprocess_amharic_text(raw_text)
        processed_rows.append({
            'channel': row.get('channel'),
            'message_id': row.get('message_id'),
            'date': row.get('date'),
            'sender_id': row.get('sender_id'),
            'media_type': row.get('media_type'),
            'media_path': row.get('media_path'),
            'clean_text': clean,
            'tokens': tokens,  # Store tokens as space-separated string
        })
    return pd.DataFrame(processed_rows)

def custom_clean_amharic(text):
    """
    Custom cleaner for Amharic text:
    - Keeps Amharic characters, numbers, and basic punctuation (፡።፣፤፥፦፧፨, . , ! ?)
    - Removes Latin and other scripts
    - Normalizes whitespace
    """
    if not isinstance(text, str):
        return ''
    # Keep Amharic, numbers, and basic punctuation
    cleaned = re.findall(r'[\u1200-\u137F0-9]+', text)
    cleaned_text = ' '.join(cleaned)
    # Normalize whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def custom_preprocess_amharic_text(text):
    """
    Returns cleaned and tokenized Amharic text (space-separated tokens)
    """
    cleaned = custom_clean_amharic(text)
    tokens = cleaned.split()
    return cleaned, ' '.join(tokens)
