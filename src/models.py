from enum import Enum
from pydantic import BaseModel, Field

class State(Enum):
    WAITING = "WAITING"
    FLYING = "FLYING"
    IN_TRANSIT = "IN_TRANSIT"
    FINISHED = "FINISHED"

class ZoneType(Enum):
    NORMAL = "NORMAL"
    RESTRICTED = "RESTRICTED"
    PRIORITY = "PRIORITY"
    BLOCKED = "BLOCKED"


class Color(Enum):
    # May create a Color class for color(red, light) or color(red, dark) or color(red) 
    BLUE = "BLUE"
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Zone(BaseModel):
    def __init__(
            self,
            name: str,
            x_axis: int,
            y_axis: int,
            color: Color,
            priority: str,
            connection: list,
            max_drones: int,
            max_link: int,
            type: str
            ) -> None:

        self.name = name
        self.x_axis: int = x_axis
        self.y_axis = y_axis
        self.color = Color.BLUE
        self.priority = priority
        self.connection: list[Connection] | None = None 
        self.max_drones = max_drones
        self.max_link = max_link
        self.type = ZoneType.NORMAL


class Connection:
    def __init__(self) -> None:
        start_zone: Zone | None = None
        end_zone: Zone | None = None
        max_capacity: int | None = None


class MapGraph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        

class Drone:
    def __init__(self, drone_id: str, start_zone: str) -> None:
        self.id = drone_id
        self.start_zone = start_zone
        self.state = State.WAITING 