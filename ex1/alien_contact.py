from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "thelepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_data(self) -> bool:
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id needs to start with 'AC'")
        elif self.contact_type.value == "physical" and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        elif (self.contact_type.value == "telepathic"
              and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        elif (self.signal_strength > 7
              and not self.message_received):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
                )
