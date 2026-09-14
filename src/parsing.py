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

#from src.models import MapGraph

def _get_drones(drone_dict: dict[str, list[str]]) -> int | None:
    number = drone_dict.get("nb_drones")
    if number:
        return int(number[0])
    else:
        return None


def list_to_dict(lista: list[list[str]]) -> dict[str, list[str]]:
    dictionary: dict[str, list[str]] = {}

    for l in lista:
        key = l[0]
        value: list[str] = []
        for el in l:
            if el != l[0]:
                value.append(el)
        dictionary[key] = value

    return dictionary

class MapParser():
    @staticmethod
    def map_parser() -> list[list[str]]:
        with open("maps/easy/01_linear_path.txt", "r", encoding="utf-8") as f:
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
 

if __name__ == "__main__":
    lista = MapParser.map_parser()
    print(len(lista))
    #print(lista)
    elementos = list_to_dict(lista)
    print(elementos)
    print(elementos["nb_drones"])
    print(elementos.get("start_hub"))