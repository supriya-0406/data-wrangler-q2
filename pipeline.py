from validator import ExtractedLead
import json

def process_input(raw_text: str):
    # Mocking LLM extraction for demo purposes
    mock_data = {
        "company_name": "Acme Corp",
        "contact_person": "Raj Patel",
        "deal_value": 75000.0,
        "next_step": "Schedule demo",
        "source_type": "whatsapp",
        "confidence": 0.92
    }
    
    try:
        validated = ExtractedLead(**mock_data)
        return {"status": "SUCCESS", "data": validated.model_dump()}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    result = process_input("dummy text")
    print(json.dumps(result, indent=2))