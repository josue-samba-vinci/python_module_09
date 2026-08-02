from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode='after')
    def mission_validation(self) -> "SpaceMission":
        valid_crew = False
        length_crew = 0
        valid_experiment = 0
        for member in self.crew:
            length_crew + 1
            if member.rank is Rank.COMMANDER or Rank.CAPTAIN:
                valid_crew = True
            if member.years_experience > 4:
                valid_experiment + 1
            if not member.is_active:
                raise ValueError("All crew members must be active")
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not valid_crew:
            raise ValueError("Must have at least one Commander or Captain")
        if (self.duration_days > 365
           and length_crew/2 > valid_experiment):
            raise ValueError(
                "Long missions (> 365 days) "
                "need 50% experienced crew (5+ years)")


def display_space_mission(space_mission: SpaceMission) -> None:
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {space_mission.crew.count()}")
    for member in space_mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")
    print("===================================")
