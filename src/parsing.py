from enum import Enum
from pydantic import ValidationError, BaseModel
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

class Color(Enum):
    BLUE = "BLUE"
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

#from src.models import MapGraph
from src.models import MapGraph, Hub, Connection
#from .models import MapGraph
from collections import defaultdict

class MapParser():
    @staticmethod
    def get_param(name: str, params: list[dict[str, str]]) -> list[dict[str, str]]:
        elements = []
        for param in params:
            if param.get(name):
                elements.append(param)
        return elements

    @staticmethod
    def get_optionals(items: str) -> dict[str, str]:
        # Una posibilidad es usar regex para los opcionales
        print(f"input: >>>{items}<<<")
        key, sep, value = items.partition("=")
        print(f"key=>{key}< sep=>{sep}< value=>{value}<")
        if not value.isalpha() or not key.isalpha:
            raise ValueError(f"Error: optionals contains invalid chars")
        return {key: value}

    @staticmethod
    def create_hub_(hub: dict[str, str]) -> Hub:
        items = hub["hub"]
        if items is None:
            raise ValueError("Key not found")
        items = items.split()
        get_item = lambda items, i: items[i] if i < len(items) else None
        print(f"items: {items}")
        optional = items[3:]
        if optional:
            for opt in optional:
                opt = opt.lstrip("[")
                opt = opt.rstrip("]")
        else:
            raise ValueError("optional = None")

        print(f"pre-input: {optional}")
        print(MapParser.get_optionals(optional))
        new_hub = Hub.model_validate(
            {
                "name": get_item(items, 0),
                "x_axis": get_item(items, 1),
                "y_axis": get_item(items, 2),
            }
        )

        print()
        print(f"\n=== Succes creating===\nhub: {new_hub}\ntype: {type(new_hub)}")
        exit(1)
        return new_hub

    @staticmethod
    def input_parser(path: str):# -> list[list[str]]:
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
            #print(MapParser.get_param("nb_drones", params))
            #print(MapParser.get_param("hub", params))
            hubs = MapParser.get_param("hub", params)
            for hub in hubs:
                print(MapParser.create_hub_(hub))
            #print(params)
            exit(1)
            l_final = []
            for line in f:
                line_list = []
                if line.startswith("#"):
                    continue
                lineas = line.split()
                for l in lineas:
                    if l.endswith(":"):
                        l = l.replace(":", "")
                    if l:
                        line_list.append(l)
                if line_list:
                    l_final.append(line_list)
            return l_final

    @staticmethod
    def get_drones(drone_dict: dict[str, list[list[str]]]) -> int | None:
        number = drone_dict.get("nb_drones")
        if number:
            return int(number[0][0])
        else:
            raise ValueError

    @staticmethod
    def list_to_dict(raw_data: list[list[str]]) -> dict[str, list[list[str]]]:
        """ Llegaria una lista con listas en str de cada parametro"""
        #Probar a hacer dos diccionarios
    #dictionary: dict[str, list[str]] = {}
        dictionary: dict[str, list[list[str]]] = {}
        for data_list in raw_data:
            key = data_list[0]
            values = []
            for value in data_list:
                if value != data_list[0]:
                    values.append(value)
            if key not in dictionary:
                dictionary[key] = [values] #porque mypy ncesita una lista
            else:
                dictionary[key].append(values)
        return dictionary

    @staticmethod
    def create_hub(input: dict[str, str | int]) -> Hub | None:
        return Hub.model_validate(input)

    @staticmethod
    def get_hub(hub_input: list[str]) -> dict[str, str | int]:
        new_hub: dict[str, str | int] = {}
        new_hub["name"] = hub_input[0]
        new_hub["x_axis"] = int(hub_input[1])
        new_hub["y_axis"] = int(hub_input[2])
        new_hub["color"] = hub_input[3].replace("color=", "")
        return new_hub

    @staticmethod
    def get_hubs_list_v2(input: dict[str, list[list[str]]]) -> dict[str, Hub]:
        """ Busca la clave 'hub' y devuelve una lista con todos esos elementos
            -Todavia no son de tipo hub
        """

        hubs_dict: dict[str, Hub] = {}
        hubs = input.get("hub")
        start = input.get("start_hub")
        if not start:
            raise ValueError
        start_hub = start[0]
        hub_start = MapParser.get_hub(start_hub)
        hubs_dict["start"] = Hub.model_validate(hub_start)

        start = input.get("end_hub")
        if not start:
            raise ValueError
        end_hub = start[0]
        hub_end = MapParser.get_hub(end_hub)
        hubs_dict["goal"] = Hub.model_validate(hub_end)
        if hubs:
            for hub in hubs:
                new_hub: dict[str, str |int] = MapParser.get_hub(hub)
                the_hub = Hub.model_validate(new_hub)
                name = new_hub.get("name")
                if isinstance(name, str):
                    hubs_dict[name] = the_hub
                else:
                    raise ValueError
        return hubs_dict

    @staticmethod
    def get_connections(input: dict[str, list[list[str]]]) -> list[dict[str, str]]:
        conn_list = []
        conns = input["connection"]
        if conns:
            for con in conns:
                conn_dict = {}
                elements = con[0].split("-")
                conn_dict["origin_hub"] = elements[0]
                conn_dict["destiny_hub"] = elements[1]
                conn_list.append(conn_dict)
        return conn_list

    @staticmethod
    def create_connection(connection: dict[str, str], hubs: dict[str, Hub]) -> Connection:
        origin_name = connection.get("origin_hub")
        destiny_name = connection.get("destiny_hub")
        if not origin_name or not destiny_name:
            raise ValueError
        origin_hub = hubs[origin_name]
        destiny_hub = hubs[destiny_name]

        return Connection.model_validate({"origin_hub": origin_hub, "destiny_hub": destiny_hub})
    @staticmethod
    def connection_dict(connections: list[dict[str, str]], hubs: dict[str, Hub]) -> list[Connection]:
        data = []
        for conn in connections:
            data.append(MapParser.create_connection(conn, hubs))
        return data

    def get_graph(self, path: str) -> MapGraph:
        raw_input = self.input_parser(path)
        parsed_input = self.list_to_dict(raw_input)
        nb_drones = self.get_drones(parsed_input)
        start = parsed_input.get("start_hub")
        if not start: # hacer que el start sea un dict tambien
            raise ValueError("error")
        list_hubs = self.get_hubs_list_v2(parsed_input)
        data_connection = MapParser.get_connections(parsed_input)
        connections = MapParser.connection_dict(data_connection, list_hubs)
        graph = MapGraph.model_validate({
                "nb_drones": nb_drones,
                "starting_hub": list_hubs["start"],
                "hubs": list_hubs,
                "goal_hub": list_hubs["goal"],
                "connection": connections
            })
        return graph
