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

class MapParser():
    @staticmethod
    def map_parser() -> None:
        with open("maps/easy/01_linear_path.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                print(line.split(" "))
 

if __name__ == "__main__":
    MapParser.map_parser()