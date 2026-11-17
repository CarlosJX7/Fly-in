from src.models import Hub, MapGraph
from src.parsing import MapParser
from pydantic import ValidationError
import sys

def main():
    print("===========================")
    print("=== Getting Graph ===")
    try:
        graph = MapParser().get_graph(sys.argv[1])
        for element in graph:
            print(f"{element}\n")
    except (ValueError, ValidationError) as err:
        print(f"Error: {err}")
    print("===========================")

if __name__ == "__main__":
    main()