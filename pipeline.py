# pipeline.py — Q2 Orchestration: Raw Input → Validate → Output
from validator import ExtractedLead
import json

def process_messy_input(raw_text: str, source: str = "unknown") -> dict:
    """
    Simulates production pipeline:
    Raw Text → [LLM Extraction] → Validation → Structured Output
    
    For demo: LLM step is mocked with realistic test data.
    """
    # Mock LLM extraction output (replace with real API call in production)
    mock_llm_output = {
        "company_name": "Acme Corp",
        "contact_person": "Raj Patel",
        "deal_value": 75000.0,
        "next_step": "Schedule technical demo next week",
        "source_type": source,
        "confidence": 0.92
    }
    
    try:
        # Pydantic V2 validation
        validated = ExtractedLead(**mock_llm_output)
        return {
            "status": "✅ VALID",
            "data": validated.model_dump(),
            "action": "insert_into_leads_clean_table"
        }
    except Exception as e:
        return {
            "status": "❌ REJECTED",
            "error": str(e),
            "action": "route_to_review_queue",
            "debug": {
                "source_text_preview": raw_text[:100] + "...",
                "extracted_raw": mock_llm_output
            }
        }

if __name__ == "__main__":
    print("🎯 Tophawks Q2: Data Wrangling Pipeline (Pydantic V2)\n")
    
    # Load sample messy input
    with open("sample_data/raw_sample.txt", "r") as f:
        raw_input = f.read().strip()
    
    print(f"📥 Raw Input ({'whatsapp'}):\n{raw_input}\n")
    
    # Process through pipeline
    result = process_messy_input(raw_input, source="whatsapp")
    
    # Output structured result
    print("📤 Pipeline Output:")
    print(json.dumps(result, indent=2))
    
    print("\n✨ Done. In production: validated data → PostgreSQL, rejected → review_queue")
