from src.models import MapGraph, Hub, Connection


class Graph:
    def __init__(self, map_graph: MapGraph) -> None:
        pass

    def neighbours(self, hub_name: str) -> list[tuple[Hub, Connection]]:
        pass

    def hub(self, name: str) -> Hub:
        pass
