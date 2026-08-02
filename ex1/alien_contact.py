from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


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
    def validate_data(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id needs to start with 'AC'")
        elif self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        elif (self.contact_type is ContactType.TELEPATHIC
              and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        elif (self.signal_strength > 7
              and not self.message_received):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
                )
        return self


def display_alien_contact(alien_contact: AlienContact) -> None:
    print(f"ID: {alien_contact.contact_id}")
    print(f"Type: {alien_contact.contact_type.value}")
    print(f"Location: {alien_contact.location}")
    print(f"Signal: {alien_contact.signal_strength}/10")
    print(f"Witnesses: {alien_contact.witness_count}")
    if alien_contact.message_received is not None:
        print(f"Notes: {alien_contact.message_received}")
    else:
        print()
    print("===================================")


if __name__ == "__main__":
    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        contact_type=ContactType.RADIO,
        location="Area 51, Nevada",
        signal_strength=8.5,
        duration_minutes=92,
        message_received="Greetings from Zeta Reticuli",
        timestamp=datetime(2026, 8, 1),
        is_verified=True,
        witness_count=6
    )
    valid_contact.validate_data()
    print("Space alien_contact data validation")
    print("===================================")
    display_alien_contact(valid_contact)
    try:
        unvalid_contact = AlienContact(
                contact_id="AC_2024_001",
                contact_type=ContactType.TELEPATHIC,
                location="Desert, Arakis",
                signal_strength=8.5,
                duration_minutes=1000,
                message_received="Greetings from Paul",
                timestamp=datetime(2026, 8, 1),
                witness_count=2
            )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            if error["loc"]:
                print(f"{error['loc'][0]}: {error['msg']}")
            else:
                print(f"{error['msg']}")
