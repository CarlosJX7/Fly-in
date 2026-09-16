from enum import Enum
from pydantic import ValidationError
from typing import Any
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
    def input_parser(path: str) -> list[list[str]]:
        with open(path, "r", encoding="utf-8") as f:
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
    def _get_drones(drone_dict: dict[str, list[str]]) -> int | None:
        number = drone_dict.get("nb_drones")
        if number:
            return int(number[0][0])
        else:
            return None

    @staticmethod
    def list_to_dict(raw_data: list[list[str]]) -> dict[str, list[list[str]]]:
        """ Llegaria una lista con listas en str de cada parametro"""
        #Probar a hacer dos diccionarios
    #dictionary: dict[str, list[str]] = {}
        dictionary: dict[str, list[list[str]]] = {}
        print(f"lista {raw_data}")
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
        print(f"resultado {dictionary}")
        return dictionary

    @staticmethod
    def create_hub(input: dict[str, str | int]) -> Hub | None:
        return Hub.model_validate(input)

    @staticmethod
    def get_hubs_list(input: dict[str, list[str] | str]):
        """ Busca la clave 'hub' y devuelve una lista con todos esos elementos
            -Todavia no son de tipo hub
        """
        print(f"input = {input}")
        def get_hub(hub_input: list[str]) -> dict[str, str | int]:
            new_hub = {}
            new_hub["name"] = hub_input[0]
            new_hub["x_axis"] = int(hub_input[1])
            new_hub["y_axis"] = int(hub_input[2])
            new_hub["color"] = hub_input[3].replace("color=", "")
            return new_hub

        hubs = input.get("hub")
        print(hubs)
        hubs_dict = {}
        if hubs:
            for hub in hubs:
                print(f"hub : {hub}")
                print(get_hub(hub))
                #hubs_dict[new_hub.get("name")] = new_hub
        return hubs_dict

    @staticmethod
    def get_connections(input: dict[str, list[str]]):
        conns = input["connection"]
        conn_list = []
        if conns:
            for con in conns:
                conn_dict = {}
                elements = con[0].split("-")
                conn_dict["origin_hub"] = elements[0]
                conn_dict["destiny_hub"] = elements[1]
                conn_list.append(conn_dict)
        return conn_list
    @staticmethod
    def create_connection(input: dict[str, str]) -> Connection:
        return Connection.model_validate(input)

    def get_graph(self, path: str):
        raw_input = self.input_parser(path)
        raw_input = self.list_to_dict(raw_input)
        nb_drones = self._get_drones
        start = raw_input.get("start_hub")
        if not start: # hacer que el start sea un dict tambien
            raise ValueError("error")
        name = start[0][0] #sacar esto a una funcion, programable solo para start y end
        x_axis = start[0][1]
        y_axis = start[0][2]
        color = start[0][3]
        hubs = []
        list_hubs = self.get_hubs_list(raw_input)
        for h in list_hubs:
            hubs.append(h)
        graph = MapGraph.model_validate(nb_drones, None, hubs, None, )
        print(hubs)
        #self.create_hub(raw_input)


if __name__ == "__main__":
    path = "maps/easy/01_linear_path.txt"
    parser = MapParser()
    lista = parser.input_parser(path)
    print(len(lista))
    #print(lista)
    elementos = MapParser.list_to_dict(lista)
    print("print elementos")
    print(elementos)
    print()
    print("elementos[nb_drones]")
    print(parser._get_drones(elementos))
    print()
    print("elementos.get(start_hub)")
    print(elementos.get("start_hub"))
    print()
    hubs = MapParser.get_hubs_list(elementos)
    for hub in hubs:
        print(hub)

    print()
    print("Conns")
    print(MapParser.get_connections(elementos))
    print()
    print()
    print("clase")
    print(parser.get_graph(path))