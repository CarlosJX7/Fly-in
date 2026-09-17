from src.models import Hub, MapGraph
from src.parsing import MapParser


def main():
    path = "maps/easy/01_linear_path.txt"
    parser = MapParser()
    print("===========================")
    print("=== Getting Graph")
    graph = parser.get_graph(path)
    for e in graph:
        print(f"{e}\n")
    print("===========================")

if __name__ == "__main__":
    main()