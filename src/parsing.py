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

class ValidKeys(str, Enum):
    COLOR="color"
    MAX_DRONES="max_drones"
    ZONE = "zone"
    MAX_LINK_CAPACITY = "max_link_capacity"


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
    def get_optionals(items: list[str]) -> dict[str, str]:
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
            #print(MapParser.get_param("nb_drones", params))
            #print(MapParser.get_param("hub", params))
            hubs = MapParser.get_param("hub", params)
            #for hub in hubs:
            #    print(MapParser.create_hub_(hub))
            return params

    @staticmethod
    def get_drones(data: list[dict[str, str]]) -> int | None:
        for element in data:
            nb_drones = element.get("nb_drones")
            if nb_drones:
                return nb_drones
        return None

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

    @staticmethod
    def create_hubs(data: list[dict[str, str]]):
        print("\n=== Creating hub ===")
        print(f"input = >>{data}<<")
        hubs: list[Hub]
        new_hub = {}
        for d in data:
            hub = d.get("hub")
            if hub:
                print(f"Extracted >>{d}<<")
        print("=== Creating hubs end ===")
        #probar a crear una lista parseada con todos los hubs
        exit(1)

    # En esta funcion podriamos sacar cada elemento
    # parsearlo y crearlo a la vez, todo en el mismo sitio
    # y en la misma iteracion
    @staticmethod
    def parse_hubs(data: list[dict[str, str]]):
        #print(f"data input = {data}")
        for d in data:
            print(f"element in data list >>{d}<<")
        pass

    def get_graph(self, path: str) -> MapGraph:
        raw_input = self.input_parser(path)
        print(f"Obtenemos: {raw_input}")
        print("=== Obteniendo nb_drones ===")
        nb_drones = self.get_drones(raw_input)
        print(nb_drones)
        print("=== Parsing hubs -> list ===")
        self.parse_hubs(raw_input)
        exit(1)
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
