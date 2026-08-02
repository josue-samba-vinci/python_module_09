from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime


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
        valid_experiment = 0
        for member in self.crew:
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                valid_crew = True
            if member.years_experience > 4:
                valid_experiment += 1
            if not member.is_active:
                raise ValueError("All crew members must be active")
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not valid_crew:
            raise ValueError("Must have at least one Commander or Captain")
        if (self.duration_days > 365
           and len(self.crew)/2 > valid_experiment):
            raise ValueError(
                "Long missions (> 365 days) "
                "need 50% experienced crew (5+ years)")
        return self


def display_space_mission(space_mission: SpaceMission) -> None:
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {len(space_mission.crew)}")
    for member in space_mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")
    print("===================================")


if __name__ == "__main__":
    crewlist: list[CrewMember]
    try:
        sarah = CrewMember(
            member_id="001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=40,
            specialization="Mission Command",
            years_experience=20
        )
        john = CrewMember(
            member_id="002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=15
        )
        alice = CrewMember(
            member_id="003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=24,
            specialization="Engineering",
            years_experience=5
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            if error["loc"]:
                print(f"{error['loc'][0]}: {error['msg']}")
            else:
                print(f"{error['msg']}")
    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2025, 8, 1),
        duration_days=900,
        crew=[sarah, john, alice],
        budget_millions=1000
    )
    print("Space Mission Crew validation")
    print("===================================")
    display_space_mission(valid_mission)
    try:
        unvalid_mission = SpaceMission(
            mission_id="M2026_SATURN",
            mission_name="Saturn Colony Establishment",
            destination="Saturn",
            launch_date=datetime(2026, 8, 1),
            duration_days=1500000,
            crew=[alice, john],
            budget_millions=10000000000000
            )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            if error["loc"]:
                print(f"{error['loc'][0]}: {error['msg']}")
            else:
                print(f"{error['msg']}")
