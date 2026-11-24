from enum import Enum
from src.models import MapGraph, Hub, Connection


class ValidKeys(str, Enum):
    COLOR = "color"
    MAX_DRONES = "max_drones"
    ZONE = "zone"
    MAX_LINK_CAP = "max_link_capacity"


class MapParser():
    """
    Parser principal de archivos de mapas (.txt)
    para construir un objeto MapGraph.
    """
    @staticmethod
    def optionals_check(opt: str, owner: str) -> list[str]:
        opt = opt.strip()
        if not opt.endswith("]"):
            raise ValueError(f"Missing closing bracket in: {owner}")
        content = opt[:-1]
        if "[" in content or "]" in content:
            raise ValueError(f"Extra brackets found in {owner}")
        items = content.split()
        if not items:
            raise ValueError(f"Empty brackets in {owner}")
        return items

    @staticmethod
    def get_optionals(items: list[str]) -> dict[str, str | int]:
        """Extrae las parejas clave=valor"""
        elements: dict[str, str | int] = {}
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

            if valid_key in (ValidKeys.MAX_DRONES, ValidKeys.MAX_LINK_CAP):
                if not value.isdigit() or int(value) <= 0:
                    raise ValueError(
                        f"'{key}' must be a positive integer, "
                        f"for '{value}'"
                        )
                elements[valid_key.value] = int(value)
            else:
                elements[valid_key.value] = value
        return elements

    @staticmethod
    def input_parser(path: str) -> list[tuple[int, str, str]]:
        """
        Lee el archivo `.txt`, ignora comentarios (`#`) y líneas vacías,
        y devuelve una lista de diccionarios `{directiva: valor}`.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                params: list[tuple[int, str, str]] = []
                for position, line in enumerate(file, 1):
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue
                    key, sep, value = line.partition(":")
                    if not sep:
                        raise ValueError(
                            f"line {position}: "
                            f"missing ':' separator"
                            )
                    key = key.strip()
                    value = value.strip()
                    params.append((position, key, value))
                return params
        except OSError as err:
            raise ValueError(
                f"Error opening map file '{path}': "
                f"{err}"
                ) from err

    @staticmethod
    def parse_hub(value: str, is_endpoint: bool) -> Hub:
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
            raise ValueError(
                f"Coordinates for hub '{mand[0]}' "
                f"must be valid integers"
                )

        hub_params: dict[str, str | int | None] = {
            "name": mand[0],
            "x_axis": x_axis,
            "y_axis": y_axis
        }

        if sep:
            opt_list = MapParser.optionals_check(opt, mand[0])
            ops = MapParser.get_optionals(opt_list)
            if "max_link_capacity" in ops:
                raise ValueError(
                    f"'max_link_capacity' is not "
                    f"valid for hub '{mand[0]}'"
                    )
            hub_params.update(ops)

        if is_endpoint:
            hub_params["max_drones"] = None
        new_hub = Hub.model_validate(hub_params)

        print(f"Created: {new_hub}")
        return new_hub

    @staticmethod
    def register_hub(hub: Hub, hubs_dict: dict[str, Hub]) -> None:
        if hub.name in hubs_dict:
            raise ValueError(f"Duplicate hub name '{hub.name}'")
        for existing in hubs_dict.values():
            if (existing.x_axis, existing.y_axis) == (hub.x_axis, hub.y_axis):
                raise ValueError(f"Duplicate coordinates for {hub.name}")
        hubs_dict[hub.name] = hub

    @staticmethod
    def parse_connection(raw_value: str, hubs: dict[str, Hub]) -> Connection:
        """
        Transforma un string de conexión en
        una instancia validada de `Connection`.
        """
        print("\n=== Parsing connection ===")
        max_link_capacity = 1
        mandatory, sep_mand, opt = raw_value.partition("[")
        origin, sep_conn, dest = mandatory.strip().partition("-")
        origin = origin.strip()
        dest = dest.strip()
        if not sep_conn or not origin or not dest or "-" in dest or " " in origin or " " in dest:
            raise ValueError(
                f"Invalid connection format '{mandatory.strip()}':"
                f" expected '<zone1>-<zone2>'"
                )

        origin_hub = hubs.get(origin)
        destiny_hub = hubs.get(dest)
        if origin_hub is None or destiny_hub is None:
            raise ValueError(
                f"Connection '{origin}-{dest}' "
                f"references an undefined hub"
                )

        if origin == dest:
            raise ValueError(
                f"Self-connection '{origin}-{dest}'"
                f"is not allowed"
                )

        if sep_mand:
            opt_list = MapParser.optionals_check(opt, f"{origin}-{dest}")
            ops = MapParser.get_optionals(opt_list)
            if set(ops.keys()) != {"max_link_capacity"}:
                raise ValueError(
                    f"Connection '{origin}-{dest}' only accepts "
                    f"'max_link_capacity'")
            max_link_capacity = int(ops["max_link_capacity"])

        new_conn = Connection(
            origin_hub=origin_hub,
            dest_hub=destiny_hub,
            max_link_capacity=max_link_capacity
        )
        print(f"Created: {new_conn}")
        return new_conn

    def get_graph(self, path: str) -> MapGraph:
        """
        Orquesta la lectura del archivo y construye el `MapGraph`
        en una única iteración (Single-Pass).
        """
        nb_drones = None
        start_hub = None
        end_hub = None
        hubs_dict: dict[str, Hub] = {}
        connections: list[Connection] = []

        elements: list[tuple[int, str, str]] = self.input_parser(path)
        if not elements:
            raise ValueError("Empty map: no parameters found")
        number, f_key, _ = elements[0]
        if f_key != "nb_drones":
            raise ValueError(f"line {number}: first parameter not nb_drones")
        for pos, key, value in elements:
            try:
                match key:
                    case "nb_drones":
                        print("\n=== Getting nb_drones ===")
                        if nb_drones is not None:
                            raise ValueError("Duplicate 'nb_drones'")
                        if not value.isdigit() or int(value) <= 0:
                            raise ValueError(
                                f"'nb_drones' must be a positive integer,"
                                f"got '{value}'"
                                )
                        nb_drones = int(value)

                    case "start_hub":
                        if start_hub is not None:
                            raise ValueError(f"Duplicate '{key}'")
                        start_hub = self.parse_hub(value, is_endpoint=True)
                        if start_hub.name in hubs_dict:
                            raise ValueError(
                                f"Duplicate hub name "
                                f"'{start_hub.name}'"
                                )
                        hubs_dict[start_hub.name] = start_hub

                    case "hub":
                        hub = self.parse_hub(value, is_endpoint=False)
                        if hub.name in hubs_dict:
                            raise ValueError(
                                f"Duplicate hub name"
                                f" '{hub.name}'"
                                )
                        hubs_dict[hub.name] = hub

                    case "end_hub":
                        if end_hub is not None:
                            raise ValueError("Duplicate 'end_hub'")
                        end_hub = self.parse_hub(value, is_endpoint=True)
                        if end_hub.name in hubs_dict:
                            raise ValueError(
                                f"Duplicate hub name"
                                f"'{end_hub.name}'"
                                )
                        hubs_dict[end_hub.name] = end_hub

                    case "connection":
                        conn = self.parse_connection(value, hubs_dict)
                        for hub in connections:
                            if {
                                hub.origin_hub.name, hub.dest_hub.name
                                } == {
                                    conn.origin_hub.name, conn.dest_hub.name}:
                                raise ValueError(
                                    f"Duplicate connection: '"
                                    f"{conn.origin_hub.name}"
                                    f"-{conn.dest_hub.name}'"
                                )
                        connections.append(conn)

                    case _:
                        raise ValueError(f"Unknown token: '{key}'")
            except ValueError as err:
                raise ValueError(f"line {pos}: {err}") from err
        print("\n=== Creating graph ===")
        if start_hub is None or end_hub is None:
            raise ValueError("Map must contain 'start_hub' and 'end_hub'")
        graph = MapGraph.model_validate({
                "nb_drones": nb_drones,
                "start_hub": start_hub,
                "hubs": hubs_dict,
                "end_hub": end_hub,
                "connections": connections
            })
        return graph
