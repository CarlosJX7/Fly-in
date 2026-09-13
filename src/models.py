from enum import Enum

class State(Enum):
    WAITING = "WAITING"
    FLYING = "FLYING"
    IN_TRANSIT = "IN_TRANSIT"
    FINISHED = "FINISHED"

class Drone:
    def __init__(self, drone_id: str, start_zone: str) -> None:
        self.id = drone_id
        self.start_zone = start_zone
        self.state = State.WAITING 
