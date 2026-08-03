from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class Space_station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: Space_station) -> None:
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    if (station.is_operational):
        print("Status: Operational")
    else:
        print("Status: Not operational")
    if station.notes is not None:
        print(f"Notes: {station.notes}")
    else:
        print()
    print("================================")


if __name__ == "__main__":
    valid_space_station = Space_station(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2026, 8, 1)
    )
    print("Space Station Data Validation")
    print("================================")
    display_station(valid_space_station)
    try:
        invalid_space_station = Space_station(
            station_id="IAS006",
            name="International Space Station of the state of Arakis, "
            "realm of the fremens",
            crew_size=10,
            power_level=110,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 8, 1)
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            variable_name = error["loc"][0]
            print(f"{variable_name}: {error['msg']}")
