# validator.py — Pydantic V2 validation for Q2
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class ExtractedLead(BaseModel):
    """Schema for LLM-extracted lead data — Pydantic V2 compatible"""
    company_name: str = Field(..., min_length=2, max_length=200)
    contact_person: Optional[str] = Field(None, min_length=2)
    deal_value: Optional[float] = Field(None, ge=1000, le=10_000_000)
    next_step: str
    source_type: str  # "whatsapp", "excel", "pdf"
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    @field_validator('company_name')
    @classmethod
    def validate_company(cls, v: str) -> str:
        v = v.strip()
        if v.lower() in ['test', 'abc', 'demo', 'sample', 'placeholder']:
            raise ValueError("Generic company name not allowed")
        return v
    
    @field_validator('contact_person')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name too short")
        # Allow letters, spaces, dots, hyphens, apostrophes
        if not re.match(r"^[A-Za-z\s.\-']+$", v):
            raise ValueError("Name contains invalid characters")
        return v
    
    @field_validator('deal_value')
    @classmethod
    def validate_currency(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return None
        return round(v, 2)
    
    @field_validator('confidence')
    @classmethod
    def flag_low_confidence(cls, v: float) -> float:
        if v < 0.8:
            print(f"⚠️  Low confidence ({v:.2f}) — flagging for human review")
        return v

# Example usage & test
if __name__ == "__main__":
    print("🧪 Testing ExtractedLead validation (Pydantic V2)...\n")
    
    # ✅ Valid case
    try:
        valid = ExtractedLead(
            company_name="Acme Corp",
            contact_person="Jane O'Brien",
            deal_value=75000.50,
            next_step="Schedule demo call",
            source_type="whatsapp",
            confidence=0.92
        )
        print("✅ VALID:", valid.model_dump())
    except Exception as e:
        print("❌ Unexpected error:", e)
    
    print("\n" + "-"*50 + "\n")
    
    # ❌ Invalid: generic company name
    try:
        invalid = ExtractedLead(
            company_name="Test",
            contact_person="John",
            deal_value=5000.0,
            next_step="Follow up",
            source_type="excel",
            confidence=0.85
        )
        print("✅ VALID:", invalid.model_dump())
    except Exception as e:
        print(f"❌ REJECTED (expected): {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # ❌ Invalid: low confidence (triggers warning but still validates)
    try:
        low_conf = ExtractedLead(
            company_name="Beta Labs",
            contact_person="Raj",
            deal_value=12000.0,
            next_step="Send pricing",
            source_type="pdf",
            confidence=0.65  # < 0.8 → warning
        )
        print("✅ VALID (with warning):", low_conf.model_dump())
    except Exception as e:
        print("❌ Error:", e)
