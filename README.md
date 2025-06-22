# Amharic E-commerce Data Extractor: EthioMart NER Pipeline

## Overview

EthioMart aims to centralize e-commerce activity from multiple Ethiopian Telegram channels, making it easier for customers and vendors to interact in one place. This project builds a data pipeline and NER (Named Entity Recognition) system to extract key business entities (products, prices, locations, etc.) from Amharic Telegram messages, images, and documents.

---

## Project Workflow

### 1. Data Ingestion & Preprocessing

- **Connect to Telegram Channels:**  
  Use a custom Python scraper (`src/data_collection/telegram_ingestor.py`) to fetch messages, images, and documents from at least 5 Ethiopian e-commerce Telegram channels.
- **Preprocessing:**  
  - Tokenize and normalize Amharic text.
  - Clean and structure data, separating metadata (sender, timestamp) from content.
  - Store raw and preprocessed data in structured formats (JSONL, CSV).

### 2. Data Labeling (CoNLL Format)

- **Label a Subset:**  
  Manually annotate 30-50 messages for NER using the CoNLL format, labeling entities:
  - `B-Product`, `I-Product`
  - `B-LOC`, `I-LOC`
  - `B-PRICE`, `I-PRICE`
  - `O` (outside any entity)
- **Save Labeled Data:**  
  Store in a plain text file for model training.

### 3. Fine-Tune NER Model

- **Model Selection:**  
  Use pre-trained models (XLM-Roberta, bert-tiny-amharic, or afroxmlr) for Amharic NER.
- **Training:**  
  - Load labeled data.
  - Tokenize and align labels.
  - Fine-tune using Hugging Face Trainer API.
  - Evaluate using F1-score and save the best model.

### 4. Model Comparison & Selection

- **Compare Multiple Models:**  
  Fine-tune and evaluate different models (XLM-Roberta, DistilBERT, mBERT, etc.).
- **Selection Criteria:**  
  Accuracy, speed, and robustness on Amharic Telegram data.
- **Choose Best Model:**  
  Based on evaluation metrics for production use.

### 5. Model Interpretability

- **Interpret Predictions:**  
  Use SHAP and LIME to explain model decisions.
- **Analyze Difficult Cases:**  
  Identify and report on ambiguous or challenging entity extractions.

### 6. Vendor Scorecard for Micro-Lending

- **Vendor Analytics Engine:**  
  Analyze each vendor's posts to compute:
  - **Posting Frequency:** Avg. posts per week.
  - **Avg. Views per Post:** Engagement metric.
  - **Top Performing Post:** Highest view count, product, and price.
  - **Avg. Price Point:** Typical product price.
- **Lending Score:**  
  Combine metrics into a weighted score (e.g., `Score = (Avg Views * 0.5) + (Posting Frequency * 0.5)`).
- **Summary Table:**  
  Present a "Vendor Scorecard" comparing all vendors.

---

## Directory Structure
