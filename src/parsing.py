from enum import Enum
"""
# Easy Level 1: Simple linear path
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal

"""

from src.models import MapGraph, Hub, Connection

class ValidKeys(str, Enum):
    COLOR="color"
    MAX_DRONES="max_drones"
    ZONE = "zone"
    MAX_LINK_CAPACITY = "max_link_capacity"

class MapParser():

    @staticmethod
    def get_optionals(items: list[str]) -> dict[str, str | int]:
        print(f"input: >>>{items}<<<")
        elements: dict[str, str] = {}
        for item in items:
            key, sep, value = item.partition("=")
            if not sep:
                raise ValueError("Separator not found")
            print(f"key=>{key}< sep=>{sep}< value=>{value}<")
            try:
                valid_key = ValidKeys(key)
            except ValueError:
                raise ValueError("Invalid key found")
            if not value.isalpha() or not key.isalpha:
                raise ValueError(f"Error: optionals contains invalid chars = {value}")
            elements[valid_key.value] = value
        print(f"Returned: {elements}")
        return elements

    @staticmethod
    def input_parser(path: str) -> list[dict[str, str]]:
        with open(path, "r", encoding="utf-8") as f:
            params: list[dict[str, str]] = []
            for line in f:
                line = line.strip()
                param = {}
                if line.startswith("#") or not line:
                    continue
                key, sep, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                param[key] = value
                params.append(param)
            return params

    @staticmethod
    def get_drones(data: list[dict[str, str]]) -> int | None:
        for element in data:
            nb_drones = element.get("nb_drones")
            if nb_drones:
                return int(nb_drones)
        return None

    # En esta funcion podriamos sacar cada elemento
    # parsearlo y crearlo a la vez, todo en el mismo sitio
    # y en la misma iteracion
    @staticmethod
    def parse_hubs(data: list[dict[str, str]]):
        #print(f"data input = {data}")
        for d in data:
            print(f"element in data list >>{d}<<")
        pass

    @staticmethod
    def parse_connection(raw_value: str, hubs: dict[str, Hub]) -> Connection:
        pass

    def get_graph(self, path: str) -> MapGraph:

        nb_drones = None
        start_hub = None
        goal_hub = None
        end_hub = None
        hubs_dict: dict[str, Hub] = {}
        connections: list[Connection] = []

        raw_input: list[dict[str, str]] = self.input_parser(path)
        print(f"Obtenemos: {raw_input}")
        for element in raw_input:
            for key, value in element.items():
                match key:
                    case "nb_drones":
                        print("\n-Getting nb_drones")
                        print(f"key = {key}")
                        print(f"value = {value}")
                        nb_drones = int(value)
                        print(f">>>{value} type:{type(nb_drones)}")
                    case "start_hub":
                        print("\n-Getting start_hub")
                        print(f"key = {key}")
                        hub = value.split(" ")
                        print(f"value = {hub}")
                        new_hub = Hub.model_validate({
                            "name": hub[0],
                            "x_axis": hub[1],
                            "y_axis": hub[2]
                        })
                        print(f">>>{new_hub} type={type(new_hub)}")
                    case "hub":
                        print("\n-Getting hub...")
                        print(f"key = {key}")
                        print(f"value = {value}")
                    case "connection":
                        pass
        exit(1)
        print("=== Parsing hubs -> list ===")
        self.parse_hubs(raw_input)
        graph = MapGraph.model_validate({
                "nb_drones": nb_drones,
                "starting_hub": list_hubs["start"],
                "hubs": list_hubs,
                "goal_hub": list_hubs["goal"],
                "connection": connections
            })
        return graph

