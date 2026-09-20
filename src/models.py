from enum import Enum
from pydantic import BaseModel, Field

class State(Enum):
    WAITING = "WAITING"
    FLYING = "FLYING"
    IN_TRANSIT = "IN_TRANSIT"
    FINISHED = "FINISHED"

class HubType(Enum):
    NORMAL = "NORMAL"
    RESTRICTED = "RESTRICTED"
    PRIORITY = "PRIORITY"
    BLOCKED = "BLOCKED"


class Color(Enum):
    BLUE = "BLUE"
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Hub(BaseModel):
    name: str = Field(...)
    x_axis: int = Field(...)
    y_axis: int = Field(...)
    color: str = "black"
    max_drones: int | None = Field(None, gt=0)
    zone_type: str | None = "normal"


class Connection(BaseModel):
    origin_hub: Hub | None = Field(...)
    destiny_hub: Hub | None = Field(...)


class MapGraph(BaseModel):
    nb_drones: int = Field(..., gt=0)
    starting_hub: Hub = Field(...)
    hubs: dict[str, Hub] = Field(...)
    goal_hub: Hub = Field(...)
    connection: list[Connection] = Field(...)


class Drone:
    def __init__(self, drone_id: str, start_hub: str) -> None:
        self.id = drone_id
        self.start_hub = start_hub
        self.state = State.WAITING