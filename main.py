from src.models import Hub, MapGraph
from src.parsing import MapParser
from pydantic import ValidationError

def main():
    path = "maps/easy/01_linear_path.txt"
    print("===========================")
    print("=== Getting Graph ===")
    try:
        graph = MapParser().get_graph(path)
    except (ValueError, ValidationError) as err:
        print(f"Error: {err}")
    for element in graph:
        print(f"{element}\n")
    print("===========================")

if __name__ == "__main__":
    main()