# 🧹 Tophawks Q2: Data Wrangling & Validation Pipeline

Transforms messy field reports (WhatsApp, Excel, PDFs) into structured, validated data ready for CRM/SQL ingestion.

## ✨ Features
- **Multi-source ingestion**: Handles raw text, Excel, and PDF inputs
- **LLM Extraction**: Strict JSON output with confidence scoring
- **Pydantic Validation**: Business rules, type enforcement, range checks
- **Human-in-the-Loop Fallback**: Auto-routes low-confidence records for review

## 🚀 How to Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run pipeline
python pipeline.py