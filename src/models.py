from enum import Enum
from pydantic import BaseModel, Field

class State(Enum):
    WAITING = "WAITING"
    FLYING = "FLYING"
    IN_TRANSIT = "IN_TRANSIT"
    FINISHED = "FINISHED"

class HubType(str, Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

class Hub(BaseModel):
    name: str = Field(...)
    x_axis: int = Field(...)
    y_axis: int = Field(...)
    color: str | None = None
    max_drones: int | None = Field(1, gt=0)
    zone: HubType = HubType.NORMAL


class Connection(BaseModel):
    origin_hub: Hub = Field(...)
    destiny_hub: Hub = Field(...)
    max_link_capacity: int = Field(1, gt=0)


class MapGraph(BaseModel):
    nb_drones: int = Field(..., gt=0)
    starting_hub: Hub = Field(...)
    hubs: dict[str, Hub] = Field(...)
    end_hub: Hub = Field(...)
    connection: list[Connection] = Field(...)


class Drone:
    def __init__(self, drone_id: str, start_hub: str) -> None:
        self.id = drone_id
        self.start_hub = start_hub
        self.state = State.WAITING