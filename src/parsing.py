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

class Color(Enum):
    BLUE = "BLUE"
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

#from src.models import MapGraph
from src.models import MapGraph, Hub
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
    def list_to_dict(lista: list[list[str]]) -> dict[str, list[str]]:
    #dictionary: dict[str, list[str]] = {}
        dictionary = defaultdict(list)

        for l in lista:
            key = l[0]
            value: list[str] = []
            for el in l:
                if el != l[0]:
                    value.append(el)
            dictionary[key].append(value)

        return dictionary

    @staticmethod
    def get_hubs(input: dict[str, list[str]]) -> list[str | int]:
        """ Busca la clave 'hub' y devuelve una lista con todos esos elementos """
        hubs = input.get("hub")
        hubs_list = []
        if hubs:
            for hub in hubs:
                new_hub = {}
                new_hub["name"] = hub[0]
                new_hub["x_axis"] = int(hub[1])
                new_hub["y_axis"] = int(hub[2])
                new_hub["color"] = hub[3].replace("color=", "")
                hubs_list.append(new_hub)
        return hubs_list

    @staticmethod
    def get_connections(input: dict[str, list[str]]):
        conns = input["connection"]
        conn_list = []
        if conns:
            for con in conns:
                conn_dict = {}
                elements = con[0].split("-")
                conn_dict["origin"] = elements[0]
                conn_dict["destiny"] = elements[1]
                conn_list.append(conn_dict)
        return conn_list

    @staticmethod
    def create_hub(input: dict[str, list[str]]):
        print("e")
        print(input)
        print("a")
        name = input.get("name")
        print(name)

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
        new_hub = Hub(
            name = name,
            x_axis = int(x_axis),
            y_axis = int(y_axis),
            color = color
            )
        print("new_hub")
        print(new_hub)
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
    hubs = MapParser.get_hubs(elementos)
    for hub in hubs:
        print(hub)

    print()
    print("Conns")
    print(MapParser.get_connections(elementos))
    print()
    print()
    print("clase")
    print(parser.get_graph(path))