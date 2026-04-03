# q2_validator.py — Sample validation logic
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ExtractedLead(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_person: Optional[str]
    deal_value: Optional[float] = Field(None, ge=1000, le=10_000_000)
    next_step: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    @validator('contact_person')
    def validate_name(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError("Name too short")
        return v.strip() if v else None
    
    @validator('deal_value')
    def validate_currency(cls, v):
        return round(v, 2) if v is not None else None