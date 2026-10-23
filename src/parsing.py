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
    """
    Parser principal de archivos de mapas (.txt) para construir un objeto MapGraph.
    """
    @staticmethod
    def get_optionals(items: list[str]) -> dict[str, str]:
        """Extrae las parejas clave=valor"""
        elements: dict[str, str] = {}
        for item in items:
            key, sep, value = item.partition("=")
            if not sep or not key or not value:
                raise ValueError(f"Separator '=' not found in '{item}'")
            try:
                valid_key = ValidKeys(key)
            except ValueError:
                raise ValueError(f"Invalid key found: '{key}'")

            if valid_key.value in elements:
                raise ValueError(f"Duplicate optional key: '{key}'")

            elements[valid_key.value] = value
        return elements

    @staticmethod
    def input_parser(path: str) -> list[dict[str, str]]:
        """
        Lee el archivo `.txt`, ignora comentarios (`#`) y líneas vacías,
        y devuelve una lista de diccionarios `{directiva: valor}`.
        """
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
    def parse_hub(value: str) -> Hub:
        """
        Transforma la definición de un hub en una instancia validada de `Hub`.
        """
        mandatory, sep, opt = value.partition("[")
        print("\n=== Getting hub ===")
        mandatory = mandatory.strip()
        mand = mandatory.split()
        if len(mand) != 3:
            raise ValueError(
                f"Invalid hub definition '{mandatory}'"
                f"Expected '<name> <x> <y>'"
                )
        if "-" in mand[0]:
            raise ValueError(f"Invalid hub name '{mand[0]}': forbidden char")
        try:
            x_axis = int(mand[1])
            y_axis = int(mand[2])
        except ValueError:
            raise ValueError(f"Coordinates for hub '{mand[0]}' must be valid integers")
        hub_params: dict[str, str | int] = {
            "name": mand[0],
            "x_axis": x_axis,
            "y_axis": y_axis
        }
        if sep:
            opt = opt.strip()
            if not opt.endswith("]"):
                raise ValueError(f"Missing closing bracket ']' in hub '{mand[0]}'")
            opt_list = opt.rstrip("]").split()
            if not opt_list:
                raise ValueError(f"Empty brackets '[]' in hub '{mand[0]}'")
            ops = MapParser.get_optionals(opt_list)
            hub_params.update(ops)
        new_hub = Hub.model_validate(hub_params)
        print(f"Created: {new_hub}")
        return new_hub

    @staticmethod
    def parse_connection(raw_value: str, hubs_dict: dict[str, Hub]) -> Connection:
        """
        Transforma un string de conexión en una instancia validada de `Connection`.
        """
        print("\n=== Parsing connection ===")
        max_link_capacity = None
        mandatory, sep_mand, opt = raw_value.partition("[")
        origin, sep_conn, dest = mandatory.strip().partition("-")
        origin = origin.strip()
        dest = dest.strip()
        if not sep_conn or not origin or not dest or "-" in dest or " " in origin or " " in dest:
            raise ValueError(f"Invalid connection format '{mandatory.strip()}': expected '<zone1>-<zone2>'")
        origin_hub = hubs_dict.get(origin)
        destiny_hub = hubs_dict.get(dest)
        if origin_hub == None or destiny_hub == None:
            raise ValueError(f"Connection '{origin}-{dest}' references an undefined hub")
        if origin == dest:
            raise ValueError(f"Self-connection '{origin}-{dest}' is not allowed")
        if sep_mand:
            opt = opt.strip()
            if not opt.endswith("]"):
                raise ValueError(f"Missing closing bracket ']' in connection '{origin}-{dest}'")
            opt_list = opt.rstrip("]").split()
            ops = MapParser.get_optionals(opt_list)
            if set(ops.keys()) != "max_link_capacity":
                raise ValueError(f"Connection '{origin}-{dest}' only accepts 'max_link_capacity'")
            max_link_capacity = int(ops["max_link_capacity"])
        opt = opt.rstrip("]")
        key, _, value = opt.partition("=")
        if value:
            max_link_capacity = int(value)
        new_conn = Connection(
            origin_hub=origin_hub,
            destiny_hub=destiny_hub,
            max_link_capacity=max_link_capacity
        )
        print(f"Created: {new_conn}")
        return new_conn

    def get_graph(self, path: str) -> MapGraph:
        """
        Orquesta la lectura del archivo y construye el `MapGraph` en una única iteración (Single-Pass).
        """
        nb_drones = None
        start_hub = None
        end_hub = None
        hubs_dict: dict[str, Hub] = {}
        connections: list[Connection] = []

        raw_input: list[dict[str, str]] = self.input_parser(path)
        print(f"Obtenemos: {raw_input}")
        for element in raw_input:
            for key, value in element.items():
                match key:
                    case "nb_drones":
                        print("\n=== Getting nb_drones ===")
                        print(f"key = {key}")
                        print(f"value = {value}")
                        nb_drones = int(value)
                        if isinstance(nb_drones, int):
                            print("Success!")
                        else:
                            print("Error creating obj")
                    case "start_hub":
                        start_hub = self.parse_hub(value)
                        hubs_dict[start_hub.name] = start_hub
                        pass
                    case "hub":
                        hub = self.parse_hub(value)
                        hubs_dict[hub.name] = hub
                    case "end_hub":
                        end_hub = self.parse_hub(value)
                        hubs_dict[end_hub.name] = end_hub
                    case "connection":
                        conn = self.parse_connection(value, hubs_dict)
                        connections.append(conn)
        print("\n=== Creating graph ===")
        graph = MapGraph.model_validate({
                "nb_drones": nb_drones,
                "starting_hub": start_hub,
                "hubs": hubs_dict,
                "end_hub": end_hub,
                "connection": connections
            })
        return graph

