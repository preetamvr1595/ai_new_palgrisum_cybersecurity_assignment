# AI Research & Dataset Infrastructure

This document outlines the architecture for the Phase 10 AI Detector Research Environment.
The infrastructure is built to strictly separate data collection, feature engineering, and model evaluation without yet committing to a specific ML architecture.

## 1. Dataset Engineering (`datasets/scripts/`)
- **`collection.py`**: Handles pulling Human text (e.g., CommonCrawl, academic papers) and generating AI text via API prompts.
- **`cleaning.py`**: Normalizes whitespace, removes null bytes, and drops duplicated entries or extremely short samples.
- **`labeling.py`**: Uniformly assigns labels (`0=HUMAN`, `1=AI`, `2=MIXED`) and metadata (domain, word count).
- **`split_manager.py`**: Splits datasets cleanly into Train, Validation, Test, and a locked Blind Benchmark set using stratified sampling.

## 2. Feature Extraction (`ai_models/detector/features/`)
Rather than relying on black-box perplexity, this engine extracts deterministic signals:
- **`stylometry.py`**: Uses `spacy` and `textstat` to compute readability scores, sentence length variance, lexical richness, and passive voice patterns.
- **`burstiness.py`**: Computes length variance and token entropy.
- **`embeddings.py`**: Wraps embedding models (like `sentence-transformers`) for semantic clustering.

## 3. Evaluation & Tracking (`ai_models/evaluation/`)
- **`metrics.py`**: Wrapper around `scikit-learn` to uniformly compute Accuracy, F1, and ROC-AUC.
- **`error_analysis.py`**: Identifies False Positives (Human text flagged as AI) to help focus feature engineering.
- **MLflow Tracker**: Tracks hyperparameters, dataset versions, and evaluation metrics across runs to ensure reproducibility.

## Getting Started
To set up this environment:
1. `cd ai_models`
2. `pip install -r requirements.txt`
3. Download the `spacy` model: `python -m spacy download en_core_web_sm`
4. Start MLflow tracking server: `mlflow ui`
